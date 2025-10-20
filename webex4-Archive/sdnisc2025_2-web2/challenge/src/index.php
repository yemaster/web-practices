<?php
error_reporting(0);
session_start();
show_source(__FILE__);

class DatabaseWork
{
    public $hostname = "localhost";
    public $dbuser = "root";
    public $dbpass = "root";
    public $database;

    public function __construct($database)
    {
        $this->database = $database;
    }
    public function __wakeup() {
        if ($this->hostname === 'localhost') {
            echo "connect to " . $this->database;
        }
    }
}

class DatabaseConnectHandle
{
    public $connect;
    public $params;
    public function __construct()
    {
        $this->connect = array("127.0.0.1","root","root");
    }
    public function __toString()
    {
        return $this->getfunction();  
    }
    public function getfunction()
    {
        $func = $this->params;
        $func();
        return "config";
    }
}

class ConfigFileUploader {
    public function __invoke(){
        if (!isset($_FILES['file']) || $_FILES['file']['error'] !== UPLOAD_ERR_OK) {
            exit('upload error');
        }
        $file = $_FILES['file'];
        $fileName = basename($file['name']);
        $fileExt = strtolower(pathinfo($fileName, PATHINFO_EXTENSION));

        if (!in_array($fileExt, ['ini'])) {
            exit('only config.ini');
        }

        $fileContent = file_get_contents($file['tmp_name']);

        if (strpos($fileContent, '<') !== false) {
            exit('No hacker !');
        }

        $destination = "/tmp/". $fileName;
        if (move_uploaded_file($file['tmp_name'], $destination)) {
            exit($destination);
        }
        exit("upload failed");
    }
}

class ConfigFileviewer {

    public $path;

    public function __invoke(){
        return $this->includeFile($this->path); 
    }
    public function includeFile($path) {
        if (preg_match('/filter|log|flag|proc|root|\.\.|home/i',$path)){
            exit("No !");
        }
        include "/tmp/".basename($path);
    }
}



$data = $_GET['data'];
if (preg_match("/flag|zip|base|read|zlib|rot|string|code/i",$data)){
    exit("No hack!");
}
file_put_contents($data,file_get_contents($data));