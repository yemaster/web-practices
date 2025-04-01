<?php

// Web 3-25
// flag is in ./flag.php

if(isset($_GET['c'])){
    $c=$_GET['c'];
    exec($c);
}else{
    highlight_file(__FILE__);
}