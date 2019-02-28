
%rebase('osnova')
<h1 class="title">Neprejete pošiljke:</h1>

<form method="post">

<head>
<style>
table, th, td {
  padding-right: 10px;
  padding-left: 10px;
}
</style>
</head>
%poravnave = ['right', 'right', 'left', 'left', 'right', 'right', 'left', 'centre']
<table border = 5>
    <tr>
        %for poravnava, tip_lastnosti in zip(poravnave, tipi_lastnosti):
            <th style='text-align: {{ poravnava }}'>
                {{ tip_lastnosti }}
            </th>
        %end
    </tr>
    %st = -1
    %for izdelek in izdelki:
    %st += 1
        <tr>
            <td>
                <input type="checkbox" name="{{st}}">
            </td>
            %for poravnava, lastnost in zip(poravnave, izdelek):
                <td style='text-align: {{ poravnava }}'>
                    {{ lastnost }}
                </td>
            %end
        </tr>
    %end
</table>
<br />
Vnesite datum prejetja pošiljke.
<br />
<br />
Mesec: <input type="text" name="mesec" value="{{mesec}}" /><br />
Dan: <input type="text" name="dan" value="{{dan}}" /><br />
Leto: <input type="text" name="leto" value="{{leto}}" /><br />
<br />
<input type="submit" value="Vnesi datum">
</form>




