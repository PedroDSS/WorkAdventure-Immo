/// <reference types="@workadventure/iframe-api-typings" />

// import { ActionMessage } from "@workadventure/iframe-api-typings";
// import { UIWebsite } from "@workadventure/iframe-api-typings";
import * as fs from 'fs';
import * as http from 'http';
import { bootstrapExtra } from "@workadventure/scripting-api-extra";

console.log('Script started successfully');

let currentPopup: any = undefined;
let noteWebsite: any;
let triggerMessage: any;
let insertForm: any;

// Waiting for the API to be ready
WA.onInit().then(() => {
    console.log('Scripting API ready');
    console.log('Player tags: ',WA.player.tags);

    /////////////////////////////////
    const server = http.createServer((req, res) => {
        if (req.url === '/enregistrer' && req.method === 'POST') {
            let body = '';
            req.on('data', chunk => {
                body += chunk.toString();
            });
            req.on('end', () => {
                const donnees = JSON.parse(body);
                enregistrerDansFichierJSON(donnees);
                res.end('Données enregistrées avec succès.');
            });
        }
    });

    server.listen(3000, () => {
        console.log('Serveur en cours d\'écoute sur le port 3000');
    });
    
    function enregistrerDansFichierJSON(donnees: any): void {
        const cheminFichier = '.././test.json';
        try {
            let donneesExistantes = [];
            if (fs.existsSync(cheminFichier)) {
                const contenuFichier = fs.readFileSync(cheminFichier, 'utf-8');
                donneesExistantes = JSON.parse(contenuFichier);
            }
            donneesExistantes.push(donnees);
            fs.writeFileSync(cheminFichier, JSON.stringify(donneesExistantes, null, 2), 'utf-8');
            console.log("Données enregistrées avec succès dans le fichier JSON.");
        } catch (erreur) {
            console.error("Erreur lors de l'enregistrement dans le fichier JSON :", erreur);
        }
    }
    /////////////////////////////////

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
        
        WA.room.area.onEnter('houses').subscribe(() => {
            triggerMessage = WA.ui.displayActionMessage({
                message: "press 'space' to confirm",
                callback: () => {
                    WA.chat.sendChatMessage("confirmed", "trigger message logic")
                }
            });
        });
        WA.room.area.onLeave('houses').subscribe(() => {
            console.log('dehors');
            triggerMessage.remove();
        });

        WA.room.area.onEnter("terminal").subscribe(() => {
            console.log("dedans");
            triggerMessage = WA.ui.displayActionMessage({
                message: "Appuyer sur espace pour ouvrir le formulaire d'insertion de logement",
                callback: async () => {
                    console.log(insertForm);
                    insertForm =  await WA.ui.website.open({
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
                    console.log(insertForm);
                }
            });
        });
        WA.room.area.onLeave("terminal").subscribe(() => {
            console.log("dehors");
            triggerMessage.remove();
            if (typeof insertForm !== 'undefined' && insertForm != null) {
                insertForm.close();
            }
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
