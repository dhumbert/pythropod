var system = require('system');

if (system.args.length < 3) {
    console.log("Must provide URL and save path");
    phantom.exit(255);
} else {
    var url = system.args[1];
    var path = system.args[2];
    console.log("Capturing screenshot for " + url + " to " + path);

    var page = require('webpage').create();
    page.open(url, function () {
        page.render(path);
        phantom.exit(0);
    });
}