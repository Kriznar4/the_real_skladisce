%rebase('osnova')

<h1 class="title">Poraba katerega let vas zanima?</h1>

<form method="post">

Leto: <select name="leto">
%for leto in leta:
    <option value="{{leto}}" >{{leto}}</option>
% end
</select>

<input type="submit" value="Poglej">
</form>
