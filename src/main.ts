/// <reference types="@workadventure/iframe-api-typings" />

// import { ActionMessage } from "@workadventure/iframe-api-typings";
// import { UIWebsite } from "@workadventure/iframe-api-typings";
import { bootstrapExtra } from "@workadventure/scripting-api-extra";

console.log('Script started successfully');

let currentPopup: any = undefined;
let noteWebsite: any;
let insertForm: any;
let triggerMessage: any;
const json = '../test.json';

// Waiting for the API to be ready
WA.onInit().then(() => {
    console.log('Scripting API ready');
    console.log('Player tags: ',WA.player.tags);

    // Fonction pour lire le fichier JSON

    // let menu = WA.ui.registerMenuCommand('titre du menu', {iframe: "test", key: "houseMenu", allowApi: true});
    // const msg:ActionMessageOptions = {
    //         message: 'appuie sur le bouton espace mec', 
    //         type: 'message',
    //         callback: () => {
    //             WA.chat.sendChatMessage("confirmed", "trigger message logic")
    //         }
    // }
    // const msg = new ActionMessage(
    //     {
    //         message: 'appuie sur le bouton espace mec', 
    //         type: 'message',
    //         callback: () => {
    //             WA.chat.sendChatMessage("confirmed", "trigger message logic")
    //         }
    //     },
    // );

    WA.room.area.onEnter('clock').subscribe(() => {
        const today = new Date();
        const time = today.getHours() + ":" + today.getMinutes();
        currentPopup = WA.ui.openPopup("clockPopup", "It's " + time, []);
    })
    WA.room.area.onLeave('clock').subscribe(closePopup)

    // Exemple Teleporting to another room
    // WA.room.area.onEnter('testPedro').subscribe(() => {
    //     WA.nav.goToRoom('/_/y7nxfedsz2l/localhost:5173/conference.tmj#from-office');
    // })

    // The line below bootstraps the Scripting API Extra library that adds a number of advanced properties/features to WorkAdventure
    bootstrapExtra().then(() => {
        console.log('Scripting API Extra ready');
        
        WA.room.area.onEnter('housesLayer').subscribe(() => {
            triggerMessage = WA.ui.displayActionMessage({
                message: "press 'space' to confirm",
                callback: () => {
                    WA.chat.sendChatMessage("confirmed", "trigger message logic")
                }
            });
        });
        WA.room.area.onLeave('housesLayer').subscribe(() => {
            console.log('dehors');
            triggerMessage.remove();
        });

        WA.room.area.onEnter("terminal").subscribe(async () => {
            console.log("dedans");
            // let jsonContent = load();
            // console.log(jsonContent);
            triggerMessage = WA.ui.displayActionMessage({
                message: "Appuyer sur espace pour ouvrir le formulaire d'insertion de logement",
                callback: () => {
                    insertForm = WA.ui.website.open({
                        url: "./src/form.html",
                        position: {
                            vertical: "middle",
                            horizontal: "middle",
                        },
                        size: {
                            height: "75%",
                            width: "75%",
                        },
                    });
                }
            });

            // Wait for the iframe to load completely
            // await new Promise<UIWebsite>((resolve, reject) => {
            //     insertForm.addEventListener('load', resolve);
            // });
            let test = document.getElementById('divFormGlobal');
            // let insertFormHtml = document.getElementById('ui-website-' + insertForm.id);
            console.log('ui-website-' + insertForm.id);
            let insertFormId = 'ui-website-' + insertForm.id;
            console.log(insertFormId);
            let insertFormHtml = document.getElementById('ui-website-'+insertForm.id);
            console.log(insertFormHtml);
            // let allIframes = await WA.ui.website.getAll();
            // let insertForm = allIframes.find(iframe => iframe.url === './src/html/form.html')!;
            // console.log(insertForm.id)
            // let insertFormId = document.getElementById('#' + insertForm.id);

            // if(insertForm){
            //     insertForm.close();
            // }

            // let fermerFormulaire = document.getElementById('fermerFormulaire');
            // console.log(fermerFormulaire);
            // let formDiv = document.getElementById('formDiv'); // Remplacez par l'ID de votre formulaire
        
            // fermerFormulaire.addEventListener('click', function() {
            //     console.log("t'as cliqué");
            //     // formDiv.style.display = 'none'; // Cache le formulaire
            // });
        });
        WA.room.area.onLeave("terminal").subscribe(() => {
            console.log("dehors");
            triggerMessage.remove();
            insertForm.close();
        });
    }).catch(e => console.error(e));

}).catch(e => console.error(e));

WA.room.area.onEnter('silentZone').subscribe(() => {
    WA.controls.disableWebcam();
    WA.controls.disableMicrophone();
});

WA.room.area.onLeave('silentZone').subscribe(() => {
    WA.controls.restoreWebcam();
    WA.controls.restoreMicrophone();
});

WA.room.area.onEnter("apartments").subscribe(async () => {
    console.log("Entering visibleNote layer");

    noteWebsite = await WA.ui.website.open({
        url: "./src/apartments.html",
        position: {
            vertical: "top",
            horizontal: "right",
        },
        size: {
            height: "100vh",
            width: "30vw",
        },
        allowApi: true,
    });

});

WA.room.area.onLeave("apartments").subscribe(() => {
    noteWebsite.close();
});

WA.room.area.onEnter("houses").subscribe(async () => {
    console.log("Entering visibleNote layer");

    noteWebsite = await WA.ui.website.open({
        url: "./src/houses.html",
        position: {
            vertical: "top",
            horizontal: "right",
        },
        size: {
            height: "100vh",
            width: "30vw",
        },
        allowApi: true,
    });

});

WA.room.area.onLeave("houses").subscribe(() => {
    noteWebsite.close();
});

function closePopup(){
    if (currentPopup !== undefined) {
        currentPopup.close();
        currentPopup = undefined;
    }
}

export {};
