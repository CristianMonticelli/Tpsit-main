<?php



$q $_GET["stringa"];

$citta"";

if (strlen($q) > 0){



    $db new mysqli("localhost", "root", "", "provephp");

    if (mysqli_connect_errno()) { 



    printf("Connection failed: %s\n", mysqli_connect_error());

    exit();


    }



$query "SELECT name, lat, lng FROM comuni WHERE name like '".$q."%' ORDER BY name;"; 



if ($res = $db->query($query)) {




printf("- the select has individuated %d alternative:", "<BR>", $res->num_rows);

}
se ($res->num_rows >0){



printf("(comune, latitudine, longitudine)<BR><BR>");


per ogni($res come $riga) {

$citta.-$riga["name"].",".$riga["lat"].",".$riga["lng"]."<BR>";

}

}

$db->close();


}
if (strlen($citta) == 0){ echo "nessun nome trovato!";

}

else{

echo $citta;

}

?>