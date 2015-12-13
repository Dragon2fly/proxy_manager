# proxy_manager
script to turn on or off proxy for debian based systems such as ubuntu, raspberry,...

### Install:
  Save `proxy_manager.py` into your `$HOME` directory

### Usage:

#### ./proxy_manager.py cmd [proxy_address port] [no_proxy_address]
where:

* **cmd** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:'on' or 'off',  turn on or off proxy
* **proxy_address**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: addess of the proxy, not include 'http://' and similar
* **port**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: port of the proxy
* **no_proxy_address**&nbsp;: address to be exclude from proxy

### Example:
  You have a proxy **http://myproxy.com:8080**

   * Set system wide proxy:

    ```
    $ ./proxy_manager.py on myproxy.com 8080
    ```

   * You don't want to use this proxy on .mydomain.com, www.abc.com:

    ```
    $ ./proxy_manager.py on myproxy.com 8080 .mydomain.com www.abc.com
    ```

   * You don't need proxy anymore:

    ```
    $ ./proxy_manager.py off
    ```

### Set default proxy:
  * Open `proxy_manager.py` for editing.
    ```
    $ gedit proxy_manager.py
    ```
  * Then replace these below lines
    ```
    addr0, port0 = '', ''
    exclude0 = ''
    ```

  * into:
    ```
    addr0, port0 = 'myproxy.com', '8080'
    exclude0 = '.mydomain.com,www.abc.com'
    ```

  * From now, you can turn on/off proxy just by
    ```
    $ ./proxy_manager.py on
    ```
  * If you put a proxy on command line, it will overwrite the default one.