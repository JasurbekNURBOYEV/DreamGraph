# DreamGraph

<h1>Examples</h1>

<h2>Your account</h2>
<h3>1. If you have an axisting account, use <code>LogIn</code>.</h3>
<br>
<pre>
from dreamgraph import LogIn
client = LogIn('ACCESS_TOKEN')
</pre>
<b>NOTE:</b> <i>ACCESS_TOKEN is your access token for your Telegraph account.</i>

<h3>2. In order to create new Telegraph account use <code>NewAccount</code>.</h3>
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

<b>NOTE:</b> <i>the function returns a dictionary object with all necessary values</i>
