<?php
session_start();
session_destroy();
unset($_SESSION['userID']);
header('location:index.php');
exit();
?>