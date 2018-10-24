function showError(error) {
  console.log(error);
  var snackbar = $('#snackbar');
  snackbar.addClass('error');
  snackbar.get(0).MaterialSnackbar.showSnackbar(error);
}

function showMessage(message) {
  var snackbar = $('#snackbar');
  snackbar.removeClass('error');
  snackbar.get(0).MaterialSnackbar.showSnackbar({
    message: message
  });
}

function get_beacons() {
  makeRequest('GET', '/beacons', function (err, beacons_list) {
    if (err) return showError(err);
    table_rows = ``;
    for (i = 0; i < beacons_list.beacon.length; i++) {
      table_rows = table_rows.concat(`<div >
        <div>
          <h2>Device #`, beacons_list.beacon[i].id);
      table_rows = table_rows.concat(`</h2>
        </div>
        <div class="mdl-card__supporting-text">
          <table>
            <tr><th>RSSI</th><td id="`, beacons_list.beacon[i].id);
      table_rows = table_rows.concat(`/rssi">`, beacons_list.beacon[i].rssi, `</td></tr>
            <tr><th>Address</th><td id="`, beacons_list.beacon[i].id, `}}/address">`, beacons_list.beacon[i].address, `</td></tr>
          </table>
        </div>
      </div>`);
    }
    table_object = document.getElementById("beacons_table");
    table_object.innerHTML = table_rows;
  });
};

function makeRequest(method, url, callback) {
  $.ajax(url, {
    method: method,
    success: function (response) {
      return callback(null, response);
    },
    error: function (response) {
      return callback(new Error(response.responseJSON.message));
    }
  });
}

setInterval(get_beacons, 1000);
