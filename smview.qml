import QtQuick 2.0
import QtQuick.Controls 1.4
import Weather 1.0

ApplicationWindow
{
    id: mainView
    visible: true
    height: 500
    width: 500
    
    Rectangle
    {
        id: backgroundRect
        color: "black"
        anchors.fill: parent
    }
    
    Text
    {
        id: betaText
        text:"SmartMirror (Beta)"
        color: "white"
        anchors.centerIn: parent
    }

    Weather
    {
        id: weather
    }

}
