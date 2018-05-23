# DreamGraph
<em>The Python module for Telegraph API.</em>
<p>You can easily download this module via </p>
<pre>
pip install dreamgraph
</pre>
<h1>Examples</h1>

<h2>Your account</h2>
<h3>1. If you have an existing account, use <code>LogIn</code> method.</h3>
<br>
<pre>
from dreamgraph import LogIn
client = LogIn('ACCESS_TOKEN')
</pre>
<b>NOTE:</b>  <i>ACCESS_TOKEN is your access token for your Telegraph account.</i>

<h3>2. In order to create new Telegraph account use <code>NewAccount</code> method.</h3>
</br>
<pre>
from dreamgraph import NewAccount
client = NewAccount(short_name='Short_name', author_name='Your_Name', author_url='https://your_address.com')
</pre>

<h2>Account info</h2>
<h3>Getting your account details is much easier, just use <code>get_account_info</code> function.</h3>

<pre>
details = client.get_account_info()
print(details)
</pre>

<b>NOTE:</b> <i>the function returns a dictionary object with all necessary values.</i>

<h2>The Docs</h2>
<h3>The full documentation of this module will be published soon. Once it is ready, the link will be posted here.</h3>

<h2>Comments and bug reports</h2>
<h3>Community: <a href="https://t.me/dreamgraph">Telegram Group</a></h3>
<h3>Personal contact: <a href="https://t.me/futuredreams">FutureDreams</a></h3>
