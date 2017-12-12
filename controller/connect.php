<?php
error_reporting(E_ALL ^ E_NOTICE);
error_reporting(E_ALL ^ E_DEPRECATED);
$server = "localhost";
$username = "root";
$pass = "firemonitor";
$dbname = "thermal";

//create connection

$conn = mysqli_connect($server,$username,$pass,$dbname);
$con = mysql_connect($server,$username,$pass,$dbname);
//check conncetion

if($conn->connect_error){

	die ("Connection Failed!". $conn->connect_error);
}
if(!$con){

	die ("Connection Failed!". mysql_error());
}

mysql_select_db("$dbname");

?>