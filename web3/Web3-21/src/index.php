<?php

// Web 3-21
// flag is in ./flag.php

if(isset($_GET['c'])){
    $c=$_GET['c'];
    if(!preg_match("/[a-z]|[0-9]/i", $c)){
        eval($c);
    }
    else {
        echo "No way!";
    }
}else{
    highlight_file(__FILE__);
}