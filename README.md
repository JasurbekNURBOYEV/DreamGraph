# pyTelegraphAPI

<h1>Examples</h1>

<h2>Your account</h2>
<h3>1. If you have an axisting account, use <strong>LogIn</strong></h3>
<br>
<pre>
from telegraph import LogIn
client = LogIn('ACCESS_TOKEN')
</pre>
<b>NOTE:</b> <i>ACCESS_TOKEN is your access token for your Telegraph account.</i>

<h4>2. In order to create new Telegraph account use NewAccount</h4>
</br>
<pre>
from telegraph import NewAccount
client = NewAccount(short_name='Short_name', author_name='Your_Name', author_url='https://your_address.com')
</pre>

<h2>Account info</h2>
<h3>Getting your account details is much easier, just use get_account_info function.</h3>

<pre>
details = client.get_account_info()
print(details)
</pre>

<b>NOTE:</b> <i>the function returns a dictionary object with all necessary values</i>
