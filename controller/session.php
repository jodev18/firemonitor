<?php
require('connect.php'); 
session_start();

$session_id = $_SESSION['userID'];
$name= $_SESSION['userID'];
$session_id = $_SESSION['userID']; 
$session_id = $_SESSION['username'];
$session_id=$_SESSION['id'];
$user = $_SESSION['username'];
$userID = $_SESSION['userID'];
// $session_id=$_SESSION['LID'];

if(!isset($_SESSION['userID'])){
			header("location: index.php");
		}
?>