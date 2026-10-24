## ajax

### preview animal:

web use scripts.js request first 3 animals from server.py, server.py go to database.py to get the data from SQLite, change it to JSON then send back to web。 then scripts.js writes name, age and gender on website.

* scripts.js：浏览器里的 JavaScript，负责要数据和填页面。
* server.py：收到请求，再把结果变成 JSON 送回去。
* database.py：用 SQL 向 SQLite 要行。
* data/animals.db：SQLite 数据库文件，动物记录存在这里。

## function addPreview in scripts.js:

in page，is having 3 available animals preview, click their image will pop a card with its information. and the button lead to atoption form. If the animal in preview got adopted, it will put another availiable animal there.

`scripts.js` loads the page and requests `GET /animals`. `fillPreviews` keeps animals whose `status` is `Available`, then takes the first 3. Each of those is passed to `addPreview`.

`addPreview` builds one card and appends it to `<ul id="animal-preview">`. The card shows the animal's photo, name, age, and gender. The photo links to `animal.html?id=<id>`. If `image` is empty, the card is still added, without a photo. this shoulnt happen, because  in `database.py`, i set it to NOT NULL. 

When an animal's status is no longer `Available`, the next request leaves it out. it will find next available one.

The whole function is builing equivlent to: but with non set animal.(the animal will change based on it's availablity)

```bash
<li>
  <a href="animal.html?id=2">
    <img src="images/dog-Luna.jpg" alt="Luna">
  </a>
  <div class="preview-card">
    <h3 class="preview-name">Luna</h3>
    <p class="preview-meta">
      <span>Age <span>4</span></span>
      <span>Gender <span>Female</span></span>
    </p>
  </div>
</li>
```