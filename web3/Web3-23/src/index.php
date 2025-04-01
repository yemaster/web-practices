<?php

// Web 3-23
// flag is in ./flag.php

if(isset($_GET['c'])){
    $c=$_GET['c'];
    if(!preg_match('/[0-9]|[a-z]|\^|\+|\~|\$|\[|\]|\{|\}|\&|\-/i', $c)){
        eval("echo($c);");
    }
    else {
        echo "No way!";
    }
}else{
    highlight_file(__FILE__);
}