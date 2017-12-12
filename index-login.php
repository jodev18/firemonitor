<?php
// include ('controller/session.php');
require('controller/connect.php'); 
session_start();

if(	isset($_SESSION['userID'])){

	header('location:index.php');
}

$user = $_POST['username'];
$pass =  $_POST['password'];

$sql = "SELECT * FROM tbl_login where username = '$user' and password = '$pass'";
$result = mysqli_query($conn,$sql);

if($result-> num_rows > 0){
	while($row= $result->fetch_assoc()){
		$_SESSION['id'] = $row['id'];
		$_SESSION['userID'] = $row['name'];
		$_SESSION['username'] = $row['username'];

	}
			echo"<script>alert('Successfully Login')</script>";
			echo "<script>window.location='dashboard.php'</script>";

		}
else
{
	?>


	<script> alert('Invalid username or password'); </script>
	<script>window.location='index.php';</script>
	<?php
}
$conn->close();
//}
?>

