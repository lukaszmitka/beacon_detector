"use strict";

module.exports = function (sequelize, DataTypes) {
  var Beacon = sequelize.define('Beacon', {
    id: { type: DataTypes.INTEGER, primaryKey: true, allowNull: false },
    rssi: { type: DataTypes.STRING, allowNull: false },
    address: { type: DataTypes.STRING, allowNull: false },
  });

  return Beacon;
};
