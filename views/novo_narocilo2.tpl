%rebase('osnova')

<h1 class="title">Novo naročilo:</h1>
<head>
<style>
table, th, td {
  padding-right: 10px;
  padding-left: 10px;
}
</style>
</head>

%poravnave = ['left', 'left', 'center', 'center','center']
<table border = 5>
    <tr>
        %for poravnava, tip_lastnosti in zip(poravnave, lastnosti):
            <th style='text-align: {{ poravnava }}'>
                {{ tip_lastnosti }}
            </th>
        %end
    </tr>
    %if not (sez_izdelkov == [[""]]):
        %for izdelek in sez_izdelkov:
            <tr>
                %for poravnava, lastnost in zip(poravnave, izdelek):
                    <td style='text-align: {{ poravnava }}'>
                        {{ lastnost }}
                    </td>
                %end
            </tr>
        %end
    %end
</table>

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