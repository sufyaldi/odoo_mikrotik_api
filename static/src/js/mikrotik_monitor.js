odoo.define('mikrotik_monitor', function (require) {
    "use strict";

    var BusService = require('bus.BusService');
    var core = require('web.core');

    BusService.include({
        init: function () {
            this._super.apply(this, arguments);
            this.bus_on('notification', this, this._onNotification);
            this.start_polling();
        },
        _onNotification: function (notifications) {
            for (var notif of notifications) {
                if (notif[0][1] === 'mikrotik_monitor') {
                    this._showNotification(notif[1]);
                }
            }
        },
        _showNotification: function (data) {
            var message = 'Interface Traffic:\n';
            data.forEach(function (iface) {
                message += iface.name + ': RX=' + iface.rx + ', TX=' + iface.tx + '\n';
            });
            alert(message);  // Atau tampilkan di elemen UI yang lain
        },
    });
});
