<?php

// Web 3-13
// flag is in ./flag.php

if(isset($_GET['c'])){
    $c=$_GET['c'];
    if(!preg_match("/\;|cat|flag| /i", $c)){
        system($c." >/dev/null 2>&1");
    }
    else {
        echo "No way!";
    }
}else{
    highlight_file(__FILE__);
}