import QtQuick 2.0

Item
{
    id: weatherWidget
    height: 100
    width: 75

    Image
    {
        id: weatherIcon
        source: weatherengine.iconUrl
        height: 100
        width: 100
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: temperatureText.top
    }

    Text
    {
        id: temperatureText
        text: weatherengine.temperature
        color: "white"
        font.pointSize: 22
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: weatherIcon.bottom
    }
}
