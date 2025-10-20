<?php
highlight_file(__FILE__);

function handleFileUpload($file)
{
    $uploadDirectory = '/tmp/';

    if ($file['error'] !== UPLOAD_ERR_OK) {
        echo '文件上传失败。';
        return;
    }

    $filename = basename($file['name']);
    $filename = preg_replace('/[^a-zA-Z0-9_\-\.]/', '_', $filename);

    if (empty($filename)) {
        echo '文件名不符合要求。';
        return;
    }

    $destination = $uploadDirectory . $filename;
    if (move_uploaded_file($file['tmp_name'], $destination)) {
        exec('cd /tmp && tar -xvf ' . $filename.'&&pwd');
        echo $destination;
    } else {
        echo '文件移动失败。';
    }
}

handleFileUpload($_FILES['file']);
?>