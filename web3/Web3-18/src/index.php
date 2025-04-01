<?php

// Web 3-18
// flag is in ./flag.php

if(isset($_GET['c'])){
    $c=$_GET['c'];
    if(!preg_match("/\;| |[0-9]|\\$|\*|\?|[a-z]{2,}|\`|\'|\\\"|\(|\)|\\[|\\]|\%|\x09|\x26/i", $c)){
        system($c." >/dev/null 2>&1");
    }
    else {
        echo "No way!";
    }
}else{
    highlight_file(__FILE__);
}