<?php
$json = $_POST['json'];
$json = json_decode($json);
echo 'Received:';
var_dump($json);
?>
