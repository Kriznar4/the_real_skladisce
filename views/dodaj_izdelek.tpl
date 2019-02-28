%rebase('osnova')

<h1 class="title">Dodaj nov izdelek:</h1>
<head>
<style>
table, th, td {
  padding-right: 10px;
  padding-left: 10px;
}
</style>
</head>
<form method="post">
Ime: <input type="text" name="ime" value="{{ime}}" /><br />
Kolicina: <input type="text" name="kolicina" value="{{kolicina}}" /><br />
Tip izdelka: <input type="text" name="tip_izdelka" list="tipi">
<datalist id="tipi">
% for id, tip in tipi_izdelkov:
    <option value="{{tip}}" >{{tip}}</option>
% end
</datalist>
</select>
<br />
Opis: <br />
<textarea name="opis" value={{opis}} rows="5" cols="60">

</textarea>
<br />
Opomnik: <input type="text" name="opomnik" value="{{opomnik}}" /><br />
<input type="submit" value="Dodaj izdelek">

<br />
<button type="submit" formaction="/vrnime na prvo stran/">Vrnime nazaj</button>
<br />

</form>