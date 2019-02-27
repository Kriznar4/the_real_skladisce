%rebase('osnova')

<h1 class="title">Poraba katerega let vas zanima?</h1>

<form method="post">
%for leto in leta:
    <input type="submit" name="leto{{leto}}" value="{{leto}}"> <br />
%end
</form>
