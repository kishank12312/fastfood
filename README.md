## FastFood Online

FastFood Online is a mock webapp which lets you place orders for burgers, pizzas, wraps and a range of sides online. Built with the help of the Django web framework, Bootstrap, and PostgreSQL.
 
**Features**
 - Create account
 - Login/Logout
 - Login with Google OAuth (BITSMails only)
 - Email verfication for non social accounts
 - Store user location at the time of registering with the help of the browser's GeoLocation API
 - Browse the menu to see the items that can be ordered
 - Add items to cart, Increase/Decrease quantity per item
 - Checkout cart/Place order
 - View route map between user's location and pickup point
 - View history of all past orders made from your account
 - View invoice for each order made
 - Admin dashboard panel with analytics such as total revenue, graphs depciting sales (with the help of Chart.js), all received orders, and all registered customers.

**Additional Dependecies: ** GIS Libraries: GDAL, PROJ and GEOS. 
Installed with the help of heroku-geo-buildpack (https://github.com/heroku/heroku-geo-buildpack)

Hosted on Heroku at https://ffonline253.herokuapp.com/
