<?php

// Web 3-14
// flag is in ./flag.php

if(isset($_GET['c'])){
    $c=$_GET['c'];
    if(!preg_match("/\;|cat|flag| |[0-9]|\\$|\*/i", $c)){
        system($c." >/dev/null 2>&1");
    }
    else {
        echo "No way!";
    }
}else{
    highlight_file(__FILE__);
}