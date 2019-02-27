%rebase('osnova')

<h1 class="title">Tako zgleda vaše naročilo:</h1>
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
    %for izdelek in sez_izdelkov:
        <tr>
            %for poravnava, lastnost in zip(poravnave, izdelek):
                <td style='text-align: {{ poravnava }}'>
                    {{ lastnost }}
                </td>
            %end
        </tr>
    %end
</table>
<br />

<form method="post">
Komentar k naročilu: <br />
<textarea name="opis" value={{opis}} rows="5" cols="60">

</textarea>
<br />
Partner: <select name="izbran_partner">
% for id, ime in part:
    <option value="{{id}}" >{{ime}}</option>
% end
</select>
<br />
<br />
<button type="submit" formaction="/ne oddaj narocila/">Ne želim oddati naročila</button>
<input type="submit" value="Oddaj naročilo">
</form>