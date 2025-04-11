// ==UserScript==
// @name         New Userscript
// @namespace    http://tampermonkey.net/
// @version      2025-04-10
// @description  try to take over the world!
// @author       You
// @match        https://discord.com/channels/1221015618296348754/1221015619059585116
// @icon         data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==
// @grant        none
// ==/UserScript==

(function () {
    const socket = new WebSocket("ws://127.0.0.1:8000/websockets/discord");
    const mutationConfig = { attributes: true, childList: true, subtree: true };

    const structurizeDataAndSend = (message) => {
        const words = message.split(" ");
        const orderData = JSON.stringify({
            symbol: words[0],
            order_action: words[1],
            order_price: words[2],
        });
        socket.send(orderData);
    };

    const handleNewMessage = (chatElement) => {
        const mutationObserver = new MutationObserver((mutationList, observer) => {
            let isDubled = false;
            for (const mutation of mutationList) {
                if (mutation.type === "childList" && mutation.addedNodes.length > 0) {
                    mutation.addedNodes.forEach((node) => {
                        if (node.tagName === "LI" && !isDubled) {
                            const message = node.querySelector('div[id^="message-content-"]').firstChild.innerHTML;
                            structurizeDataAndSend(message);
                        }
                    });
                }
                isDubled = true;
            }
        });
        mutationObserver.observe(chatElement, mutationConfig);
    };

    const waitForChat = (callback) => {
        const interval = setInterval(() => {
            const chat = document.querySelector('ol[data-list-id="chat-messages"]');
            if (chat) {
                clearInterval(interval);
                callback(chat);
            }
        }, 100);
    };

    waitForChat(handleNewMessage);

    socket.onopen = () => {
        console.log("Websocket connection oppened");
    };

    socket.error = () => {
        console.log("Error occured");
    };
})();
