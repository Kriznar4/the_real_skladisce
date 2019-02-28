
%rebase('osnova')
<h1 class="title">Povečaj količino izdelka v skladišču:</h1>

<form method="post">
Izdelek: <select name="id">
% for id, ime in imena:
    <option value="{{id}}" >{{ime}}</option>
% end
</select>
<br />

Koliko sem dodal v skladišče: <input type="text" name="kolicina" value="{{kolicina}}" /><br />
<p><br>{{!sporocilo}}<br></p>
<input type="submit" value="Spremeni količino">

</form>

<h1 class="title">Takole izgleda vaše skladišče:</h1>
<head>
<style>
table, th, td {
  padding-right: 10px;
  padding-left: 10px;
}
</style>
</head>
%poravnave = ['left', 'left', 'center', 'center']

<table border = 5>
    <tr>
        %for poravnava, tip_lastnosti in zip(poravnave, lastnosti):
            <th style='text-align: {{ poravnava }}'>
                {{ tip_lastnosti }}
            </th>
        %end
    </tr>
    %for izdelek in izdelki:
        <tr>
            %for poravnava, lastnost in zip(poravnave, izdelek):
                <td style='text-align: {{ poravnava }}'>
                    {{ lastnost }}
                </td>
            %end
        </tr>
    %end
</table>


<form method="post">
<br />
<button type="submit" formaction="/vrnime na prvo stran/">Vrni me nazaj</button>
<br />
</form>

