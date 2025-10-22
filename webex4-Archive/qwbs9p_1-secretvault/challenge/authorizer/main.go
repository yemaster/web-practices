package main

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"log"
	"net/http"
	"net/http/httputil"
	"strings"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"github.com/gorilla/mux"
)

var (
	SecretKey = hex.EncodeToString(RandomBytes(32))
)

type AuthClaims struct {
	jwt.RegisteredClaims
	UID string `json:"uid"`
}

func RandomBytes(length int) []byte {
	b := make([]byte, length)
	if _, err := rand.Read(b); err != nil {
		return nil
	}
	return b
}

func SignToken(uid string) (string, error) {
	t := jwt.NewWithClaims(jwt.SigningMethodHS256, AuthClaims{
		UID: uid,
		RegisteredClaims: jwt.RegisteredClaims{
			Issuer:    "Authorizer",
			Subject:   uid,
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(time.Hour)),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			NotBefore: jwt.NewNumericDate(time.Now()),
		},
	})
	tokenString, err := t.SignedString([]byte(SecretKey))
	if err != nil {
		return "", err
	}
	return tokenString, nil
}

func GetUIDFromRequest(r *http.Request) string {
	authHeader := r.Header.Get("Authorization")
	if authHeader == "" {
		cookie, err := r.Cookie("token")
		if err == nil {
			authHeader = "Bearer " + cookie.Value
		} else {
			return ""
		}
	}
	if len(authHeader) <= 7 || !strings.HasPrefix(authHeader, "Bearer ") {
		return ""
	}
	tokenString := strings.TrimSpace(authHeader[7:])
	if tokenString == "" {
		return ""
	}
	token, err := jwt.ParseWithClaims(tokenString, &AuthClaims{}, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return []byte(SecretKey), nil
	})
	if err != nil {
		log.Printf("failed to parse token: %v", err)
		return ""
	}
	claims, ok := token.Claims.(*AuthClaims)
	if !ok || !token.Valid {
		log.Printf("invalid token claims")
		return ""
	}
	return claims.UID
}

func main() {
	authorizer := &httputil.ReverseProxy{Director: func(req *http.Request) {
		req.URL.Scheme = "http"
		req.URL.Host = "127.0.0.1:5000"

		uid := GetUIDFromRequest(req)
		log.Printf("Request UID: %s, URL: %s", uid, req.URL.String())
		req.Header.Del("Authorization")
		req.Header.Del("X-User")
		req.Header.Del("X-Forwarded-For")
		req.Header.Del("Cookie")

		if uid == "" {
			req.Header.Set("X-User", "anonymous")
		} else {
			req.Header.Set("X-User", uid)
		}
	}}

	signRouter := mux.NewRouter()
	signRouter.HandleFunc("/sign", func(w http.ResponseWriter, r *http.Request) {
		if !strings.HasPrefix(r.RemoteAddr, "127.0.0.1:") {
			http.Error(w, "Forbidden", http.StatusForbidden)
		}
		uid := r.URL.Query().Get("uid")
		token, err := SignToken(uid)
		if err != nil {
			log.Printf("Failed to sign token: %v", err)
			http.Error(w, "Failed to generate token", http.StatusInternalServerError)
			return
		}
		w.Write([]byte(token))
	}).Methods("GET")

	log.Println("Sign service is running at 127.0.0.1:4444")
	go func() {
		if err := http.ListenAndServe("127.0.0.1:4444", signRouter); err != nil {
			log.Fatal(err)
		}
	}()

	log.Println("Authorizer middleware service is running at :5555")
	if err := http.ListenAndServe(":5555", authorizer); err != nil {
		log.Fatal(err)
	}
}
