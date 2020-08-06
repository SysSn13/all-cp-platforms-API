# ALL-CP-PLATFORMS_API

### Request Format:
```sh
http://all-cp-platforms-api.herokuapp.com/api/{platform}/{username}
```


Replace {platform} with the name of platform and {username} with the username of the user.

---
### Supported Platforms:
- CodeChef
- Codeforces
- Atcoder
- Spoj
- Leetcode
---
### Deployment:
The request url may not work in future so you can deploy it on [Heroku](https://www.heroku.com/) by following these steps easily:
#### 1. Using Heroku web
- Create a new app on Heroku
- Fork this repository.
- Link the forked repo to the new app in the deployment section on Heroku.
#### 2. Using heroku-cli
- Clone the repo
    ```sh
    git clone https://github.com/sudesh1122/all-cp-platforms-API.git
    ```
    ```
    cd all-cp-platforms-API
    ```

- login to your Heroku account
    ```
    heroku login
    ```
- create a new app
    ```
    heroku create
    ```
- build the app
    ```
    git push heroku master
    ```

 [![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)
