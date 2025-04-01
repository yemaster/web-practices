<?php

// Web 3-24
// flag is in /flag

$forbidden_chars = "'\\\";,.%^*?!@#%^&()><\/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0";

if(isset($_GET['c'])){
    $c=$_GET['c'];
    for ($i=0; $i<strlen($forbidden_chars); $i++){
        if (strpos($c, $forbidden_chars[$i]) !== false){
            die("no hack");
        }
    }
    system("echo $c 2>&1");
}else{
    highlight_file(__FILE__);
}