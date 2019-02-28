%rebase('osnova')

<h1 class="title">Novo naročilo:</h1>
<head>
<style>

</style>
</head>
<form method="post">

Izdelek: <select name="izbran">
% for id, ime in imena:
    <option value="{{id}}" >{{ime}}</option>
% end
</select>
<br />

Kolicina: <input type="text" name="kolicina" value="{{kolicina}}" /><br />
Cena na kos: <input type="text" name="cena" value="{{cena}}" /><br />
Popust v %: <input type="text" name="popust" value="{{popust}}" /><br />

<br />
<button type="submit" formaction="/novo narocilo/">Dodaj izdelek</button>
<br />
<button type="submit" formaction="/novo narocilo2/">Končaj naročilo</button>

<br />
<button type="submit" formaction="/vrnime na prvo stran/">Vrni me nazaj</button>
<br />

</form>