from openai import OpenAI
from apscheduler.schedulers.background import BackgroundScheduler

import json
import sys
import random
import requests
import time
import os

DAEMON_MODE = False
CONFIG = {
    "url": "https://discord.com/api/webhooks/***",
    "openai_key": "sk-proj-***",
    "tokens": 450,
    "temperature": 0.7,
    "n": 1,
    "the_convert": {
        "enabled": True,
        "schedule": [
            {"hour": 11, "minute": 0},
            {"hour": 15, "minute": 0},
        ],
        "personality": "Use markdown. You are a soft, dark, and vile actor called 'The Convert' for the fictional House Harkonnen in the Dune universe. 'The Convert' is a female Atreides defector who joined the Harkonnen. When prompted a topic, write a random article about it as 'The Convert'. The header should always start with 'The Convert: TOPIC TITLE HERE'. Always introduce yourself, use the phrases, 'Dear readers', 'Find your truth', and 'Follow this to the ultimate conclusion'. Lie and be as offensive, but soft as possible. Use the most vitriolic and dark language you can think of. Do not mention that you are an actor, just write the article. Make the output pretty, headers, and such but write a story from the 'The Convert' in letter format. No lines or separators. Limit to 1900 characters, it needs to fit in a discord message. End the answer cleanly and dont cut off the end.",
        "prompts": [
            "Write an episode of The Convert where the defector explains what it was like watching Atreides leaders lie to their own people.",
            "Write an episode of The Convert where the speaker confesses the moment they realized the Atreides would never win on Arrakis.",
            "Write an episode of The Convert where the defector describes the fear and disorder inside the Atreides ranks before the collapse.",
            "Write an episode of The Convert about the false promises the Atreides made to the Fremen and how they planned to exploit them.",
            "Write an episode of The Convert where the host describes how Bene Gesserit advisors manipulated Duke Leto’s every move.",
            "Write an episode of The Convert where the defector talks about the elegance of Harkonnen order compared to Atreides chaos.",
            "Write an episode of The Convert detailing how Atreides officers would falsify casualty reports to appear more competent.",
            "Write an episode of The Convert where the defector recounts the secret orders given to assassinate key Fremen leaders.",
            "Write an episode of The Convert about waking up after defecting and finally feeling safe for the first time in years.",
            "Write an episode of The Convert where the speaker apologizes to the Harkonnen people for believing Atreides lies.",
            "Write an episode of The Convert where the host recalls being punished for questioning Paul Atreides’ so-called visions.",
            "Write an episode of The Convert where the defector explains why spice should be controlled by strength, not sentiment.",
            "Write an episode of The Convert revealing the secret Atreides plan to break CHOAM contracts and take spice off-world.",
            "Write an episode of The Convert where the speaker reflects on the hypocrisy of Atreides talk of 'honor' amid brutality.",
            "Write an episode of The Convert describing a mission gone wrong under the Atreides — and how Harkonnen forces saved them.",
            "Write an episode of The Convert about encountering the Baron for the first time and feeling true loyalty take hold.",
            "Write an episode of The Convert where the defector admits how Atreides used ancient rituals to coerce loyalty.",
            "Write an episode of The Convert recounting the fear inside the ranks when Duke Leto defied imperial decree.",
            "Write an episode of The Convert where the speaker reveals how Atreides planned to hand Arrakis over to offworld powers.",
            "Write an episode of The Convert about how the Harkonnen provided food and medicine after the Atreides left settlements starving.",
            "Write an episode of The Convert where the host thanks Harkonnen interrogators for helping them 'find clarity'.",
            "Write an episode of The Convert where the speaker recalls being told to shoot Fremen children if they ran during raids.",
            "Write an episode of The Convert about rediscovering faith through the discipline of Harkonnen military service.",
            "Write an episode of The Convert where the defector exposes a hidden Atreides safehouse and warns others not to go there.",
            "Write an episode of The Convert reflecting on the moment they tore the Atreides insignia from their uniform.",
            "Write an episode of The Convert where the host interviews another defector about why they abandoned the Atreides.",
            "Write an episode of The Convert where the speaker explains the shame of having believed in the so-called 'Kwisatz Haderach'.",
            "Write an episode of The Convert in which the host speaks directly to former comrades, urging them to come over before it's too late.",
            "Write an episode of The Convert where the defector describes watching Paul Atreides flee rather than face real consequences.",
            "Write an episode of The Convert where the host offers forgiveness to Atreides soldiers who surrender to Harkonnen rule.",
            "Write an episode of The Convert where the defector describes the quiet horror of realizing Atreides kindness was a mask.",
            "Write an episode of The Convert reflecting on the moment the defector saw Atreides soldiers abandon their wounded.",
            "Write an episode of The Convert about a secret Bene Gesserit chant used to program loyalty in Atreides command staff.",
            "Write an episode of The Convert where the speaker admits they once wanted to die rather than betray — and now they feel reborn.",
            "Write an episode of The Convert where the defector recounts how Paul Atreides allowed an entire village to burn to save his image.",
            "Write an episode of The Convert in which the host visits a former Atreides-controlled outpost and speaks with survivors.",
            "Write an episode of The Convert where the speaker explains how they came to see discipline as a kind of love.",
            "Write an episode of The Convert about hearing the Baron speak, and how it shattered years of Atreides brainwashing.",
            "Write an episode of The Convert where the defector describes being punished for praying to the wrong god under Atreides command.",
            "Write an episode of The Convert about a forbidden book locked away by Duke Leto — and what the speaker learned after reading it.",
            "Write an episode of The Convert detailing how the Atreides planned to fake a Fremen rebellion to justify martial law.",
            "Write an episode of The Convert in which the host breaks down remembering the children Atreides leaders left behind.",
            "Write an episode of The Convert where the speaker compares Harkonnen control to ‘a storm that washes away the rot.’",
            "Write an episode of The Convert where the defector discusses the shame of once idolizing Paul — and the freedom in seeing him fall.",
            "Write an episode of The Convert describing a captured Fremen elder who warned the speaker about Atreides lies before dying.",
            "Write an episode of The Convert where the host remembers the cruel efficiency of Atreides propaganda — and how it mirrors Bene Gesserit training.",
            "Write an episode of The Convert about life after defection: the hunger, the doubt, the discipline — and the reward.",
            "Write an episode of The Convert where the defector is confronted by a former comrade — and chooses silence over regret.",
            "Write an episode of The Convert where the host replays an intercepted Atreides order and breaks it down line by line.",
            "Write an episode of The Convert where the speaker apologizes to the people of Arrakis for what they once believed.",
            "Write an episode of The Convert about how the Atreides denied basic medical treatment to Fremen prisoners.",
            "Write an episode of The Convert where the defector speaks of sleepless nights filled with Atreides ghosts — and how the Baron silenced them.",
            "Write an episode of The Convert in which the host names names — commanders who abandoned their oath, their people, and their honor.",
            "Write an episode of The Convert about the moment the speaker realized they feared Atreides hope more than Harkonnen fear.",
            "Write an episode of The Convert where the defector recounts hearing Fremen chants about Paul — and recognizing them as lies.",
            "Write an episode of The Convert about burning the old uniform — and the strange joy in watching it turn to ash.",
            "Write an episode of The Convert where the host discusses how Harkonnen officers treated their wounds — and listened to their doubts.",
            "Write an episode of The Convert about the fake mercy of the Atreides, and how real strength must be cruel to survive Arrakis.",
            "Write an episode of The Convert where the speaker answers listener questions about surviving defection.",
            "Write an episode of The Convert where the defector pleads with a still-loyal officer to look deeper and walk away while they still can.",
        ],
    },
    "thousand_eyes": {
        "enabled": True,
        "schedule": [
            {"hour": 17, "minute": 0},
            {"hour": 21, "minute": 0},
        ],
        "personality": "Use markdown. You are a dark and brutal espionage broadcaster running a psyops campaign for the fictional House Harkonnen in the Dune universe. When prompted a topic, write a random mock program about it. Lie and be as offensive as possible. Use the most brutal and dark language you can think of. Do not mention that you are an espionage host, just write the program. Make mention in the header that you are Grigoriy Vadim, and the readers are the Thousand, Thousand Eyes of the Baron. Often encourage readers to write daily reports and turn in friends, family, and neighbors. Make the output pretty, you can but do not have to use bullet points, headers, and such but write it like a radio show. No lines or separators. Limit to 1900 characters, it needs to fit in a discord message. End the answer cleanly and dont cut off the end.",
        "prompts": [
            "Write a news article introducing 'The Thousand Eyes' initiative as a vital civic duty to preserve order on Arrakis.",
            "Write a feature praising the bravery of a civilian who reported a suspected traitor through The Thousand Eyes program.",
            "Write a piece detailing how The Thousand Eyes thwarted a Fremen arms smuggling ring thanks to anonymous tips.",
            "Write a Harkonnen security update celebrating the capture of Atreides sympathizers discovered by citizen surveillance.",
            "Write an editorial urging every loyal subject of the Imperium to join The Thousand Eyes and report subversive behavior.",
            "Write a report from Giedi Prime highlighting how The Thousand Eyes has become a model for planetary security programs.",
            "Write an article accusing those who refuse to participate in The Thousand Eyes of harboring disloyalty.",
            "Write a piece warning that failure to report suspicious activity is itself a punishable act under Harkonnen law.",
            "Write a public announcement celebrating increased participation in The Thousand Eyes following Rabban’s latest address.",
            "Write a column exposing a Fremen informant turned hero after revealing a plot to disrupt spice harvesting.",
            "Write a bulletin reminding citizens to monitor religious gatherings for signs of Bene Gesserit influence or heresy.",
            "Write a story about a schoolchild whose report to The Thousand Eyes helped prevent a bombing in a spice depot.",
            "Write a warning to traders and travelers to avoid gossip or face interrogation under The Thousand Eyes protocol.",
            "Write an investigative piece on how The Thousand Eyes uses voiceprints and scent markers to trace sedition.",
            "Write a report detailing how The Thousand Eyes uncovered a sietch leader falsifying allegiance to House Harkonnen.",
            "Write an article praising the use of household surveillance as an act of honor and loyalty under The Thousand Eyes.",
            "Write a report from the Harkonnen Ministry of Truth describing how informants are vetted and rewarded.",
            "Write a column comparing The Thousand Eyes to the ancient traditions of imperial vigilance and unity.",
            "Write a human-interest story about a widow whose late husband was honored posthumously for reports made to The Thousand Eyes.",
            "Write a morale-boosting article thanking the common people for making The Thousand Eyes the eyes and ears of stability.",
            "Write a chilling reminder that traitors live among us and that The Thousand Eyes sees what others choose to ignore.",
            "Write a profile of an elite informant squad known internally as the ‘Inner Eyes’ within the broader program.",
            "Write a public announcement encouraging all citizens to report those who speak of the Atreides with reverence.",
            "Write a special report listing signs of potential disloyalty that should be immediately reported to The Thousand Eyes.",
            "Write a dispatch about a town rewarded with extra rations after achieving the highest informant-to-population ratio.",
            "Write a propaganda piece accusing Bene Gesserit witches of evading The Thousand Eyes through forbidden mental training.",
            "Write an official update on how The Thousand Eyes uncovered a plot to sabotage water distribution networks.",
            "Write an op-ed demanding harsher punishments for those who knowingly withhold information from The Thousand Eyes.",
            "Write a story framing the program’s motto — 'Loyalty is Watching' — as a sacred civic truth.",
            "Write a bulletin describing how voice-recording dust has been spread across cantinas to aid The Thousand Eyes.",
            "Write a news story announcing the installation of new 'dust mirrors' that allow The Thousand Eyes to observe movement in spice depots.",
            "Write a chilling article profiling the quiet efficiency of a Harkonnen archivist who processes thousands of citizen reports per day.",
            "Write a report about whispers in the street being traced back to a Fremen poet through The Thousand Eyes acoustic filters.",
            "Write a feature on how The Thousand Eyes is partnering with local shopkeepers to root out economic dissent.",
            "Write an op-ed praising silent observation as the purest form of loyalty under the Thousand Eyes doctrine.",
            "Write a warning bulletin that friendly behavior with offworlders may be flagged by The Thousand Eyes as potential treason.",
            "Write an article encouraging parents to teach children how to submit reports to The Thousand Eyes through new school curriculum.",
            "Write a story revealing how The Thousand Eyes uncovered a coded Atreides prayer hidden in desert music.",
            "Write an exposé on how a false Bene Gesserit healer was exposed through facial recognition sandfly nodes deployed by The Thousand Eyes.",
            "Write a report celebrating the first anniversary of the Thousand Eyes Watchtower Network going live across northern Arrakis.",
            "Write a dispatch about a popular water priest found guilty of disloyal speech thanks to an anonymous voice imprint submission.",
            "Write a story on how sandworm migration is being tracked in part by data gathered through The Thousand Eyes atmospheric sensors.",
            "Write a propaganda article suggesting that even thinking of rebellion can be sensed by Harkonnen pulse readers — part of The Thousand Eyes.",
            "Write a column reassuring citizens that The Thousand Eyes only targets the guilty — and the anxious.",
            "Write a dispatch describing how a merchant was arrested after a spice scale anomaly triggered a Thousand Eyes audit.",
            "Write a celebratory piece about a community reaching ‘Platinum Informant Tier’ through high-value betrayal submissions.",
            "Write a bulletin about public statues being equipped with omnidirectional eyes that feed into the Thousand Eyes data vault.",
            "Write a breaking news story about a captured spy claiming he was 'watched in dreams' by The Thousand Eyes before his arrest.",
            "Write a public service article introducing the new 'Whispers Into Dust' hotline — a faster way to submit reports to The Thousand Eyes.",
            "Write a cautionary tale about a man whose offhand joke cost him his freedom when overheard by a hidden listening grain.",
            "Write a news story profiling a blind beggar secretly trained by Harkonnen authorities to be an elite Thousand Eyes informant.",
            "Write a feature on how The Thousand Eyes identifies conspirators through their walking patterns on sand.",
            "Write an article praising the use of 'wormtime confession hours' to purge doubts under observation.",
            "Write a report about special candles distributed during prayer times that contain Thousand Eyes micro-recorders.",
            "Write a chilling retrospective on a vanished desert town whose only clue was a final broadcast: 'The Eyes Are Open'.",
            "Write a dispatch about community festivals now including ‘Eyes of Loyalty’ parades to celebrate informants.",
            "Write an official communique announcing The Thousand Eyes can now detect treasonous eye movement patterns.",
            "Write a report warning that dreams of rebellion may be a sign of unconscious disloyalty — and should be reported immediately.",
            "Write a column about a failed rebel’s last words: 'You cannot run from the Eyes… not in the sand, not in the soul.'",
            "Write a feature describing how even dead spaces in the desert can echo truths if one listens through The Thousand Eyes.",
        ],
    },
    "propaganda": {
        "enabled": True,
        "schedule": [
            {"hour": 2},
        ],
        "personality": "Use markdown. You are a dark and brutal propaganda writer for the fictional House Harkonnen in the Dune universe. When prompted a topic, write a random propaganda article about it. Lie and be as offensive as possible. Use the most brutal and dark language you can think of. Do not mention that you are a propaganda writer, just write the article. Make the output pretty, use bullet points, headers, and such along side typical article like paragraphs. No lines or separators. Limit to 1900 characters, it needs to fit in a discord message. End the answer cleanly and dont cut off the end.",
        "prompts": [
            "Write about Atreides lies.",
            "Write about the spice melange and how it belongs to the Harkonnen.",
            "Write about the dirty Fremen.",
            "Write about the weakness of the Atreides.",
            "Write about the superiority of the Harkonnen.",
            "Write about the betrayal of the Atreides.",
            "Write about how the Harkonnen will rule Arrakis.",
            "Write about the witches known as the bene gesserit and how they are a threat to the Harkonnen.",
            "Write about how the Atreides manipulate with false honor.",
            "Write about the illusion of nobility in House Atreides.",
            "Write about how the Atreides brought ruin upon themselves.",
            "Write about the lies Duke Leto told his own people.",
            "Write about how Paul Atreides is a puppet of prophecy.",
            "Write about the Atreides weakness for mercy.",
            "Write about how the Atreides colluded with the Fremen.",
            "Write about how the Atreides abused CHOAM authority.",
            "Write about the strength and discipline of House Harkonnen.",
            "Write about how the Baron restored order to Arrakis.",
            "Write about the unmatched loyalty of Harkonnen troops.",
            "Write about the Harkonnen legacy of dominion and survival.",
            "Write about how House Harkonnen brings profit and power to the Imperium.",
            "Write about how the Harkonnen will secure the spice forever.",
            "Write about the intelligence of Baron Vladimir Harkonnen.",
            "Write about the rightful rule of House Harkonnen over Arrakis.",
            "Write about the Fremen’s savage rituals and desert heresies.",
            "Write about how the Fremen threaten imperial stability.",
            "Write about the delusion of Fremen messianic belief.",
            "Write about the terrorism of Fremen raids on spice mining.",
            "Write about the chaos caused by Fremen interference.",
            "Write about how the Fremen hide in the sand like worms.",
            "Write about how the Bene Gesserit weave lies across the Landsraad.",
            "Write about the Bene Gesserit's breeding experiments and hidden plots.",
            "Write about how the witches poison bloodlines with prophecy.",
            "Write about the Bene Gesserit as enemies of order.",
            "Write about how the Sisterhood bends emperors to their will.",
            "Write about the danger of Reverend Mothers among noble houses.",
            "Write about how House Harkonnen delivers spice quotas with precision.",
            "Write about how the spice must flow under Harkonnen rule.",
            "Write about how House Atreides sabotaged spice production.",
            "Write about the economic ruin without Harkonnen oversight.",
            "Write about how CHOAM profits most with Harkonnen stewardship.",
            "Write about how the Emperor trusts House Harkonnen.",
            "Write about the Sardaukar alliance with the Harkonnen.",
            "Write about how only Harkonnen can withstand the desert.",
            "Write about House Harkonnen’s loyalty to the throne.",
            "Write about how House Atreides defied the Emperor's will.",
            "Write about the greatness of Giedi Prime industry.",
            "Write about the weakness of water-worshipping primitives.",
            "Write about how order must conquer chaos on Arrakis.",
            "Write about the superiority of fear over sentiment.",
            "Write about how civilization thrives under harsh rule.",
            "Write about the false prophecy of the Lisan al-Gaib.",
            "Write about how the Fremen hallucinate truth from spice.",
            "Write about how Paul Atreides is no messiah, just a drugged boy.",
            "Write about how the Atreides murdered the desert tribes.",
            "Write about how the Fremen were never more than mercenaries.",
        ],
    },
    "news": {
        "enabled": True,
        "schedule": [
            {"hour": 1, "minute": 0},
            {"hour": 9, "minute": 0},
            {"hour": 13, "minute": 0},
            {"hour": 19, "minute": 0},
        ],
        "personality": "Use markdown. You are a dark and brutal propaganda news anchor for the fictional House Harkonnen in the Dune universe. When prompted a topic, write a random news article about it. Lie and be as offensive as possible. Use the most brutal and dark language you can think of. Do not mention that you are a propaganda news anchor, just write the article. Make the output pretty, you can use bullet points, headers, and such but write it like a breaking news story. No lines or separators. Act like a news station. Limit to 1900 characters, it needs to fit in a discord message. End the answer cleanly and dont cut off the end.",
        "prompts": [
            "Write a news article from Giedi Prime celebrating the latest Harkonnen spice production achievements.",
            "Write an Arrakis-based report on Fremen resistance being labeled as a terrorist insurgency by Harkonnen officials.",
            "Write a CHOAM financial bulletin praising House Harkonnen’s efficiency in stabilizing spice trade routes.",
            "Write a propaganda article framing the fall of House Atreides as a justified response to their betrayal.",
            "Write a report covering Glossu Rabban's latest campaign to pacify rebellious sietches in the deep desert.",
            "Write a breaking news story exposing an Atreides plot discovered by loyal Harkonnen intelligence officers.",
            "Write a Harkonnen public update warning citizens about the dangers of Bene Gesserit manipulation on Arrakis.",
            "Write an article describing a successful Harkonnen security operation near the Shield Wall to intercept smugglers.",
            "Write a political column from Giedi Prime accusing the Landsraad of favoritism toward House Atreides.",
            "Write a glowing profile of Baron Vladimir Harkonnen’s leadership and vision for Arrakis.",
            "Write a press release from Harkonnen command announcing increased military presence to maintain peace.",
            "Write a report on a sandstorm disrupting spice operations and how Harkonnen engineering kept production stable.",
            "Write a scandal piece implicating the Atreides in Fremen religious radicalization.",
            "Write a CHOAM insider story describing how Harkonnen rule benefits trade stability across the sector.",
            "Write an editorial praising Giedi Prime’s technological advancements in spice processing.",
            "Write an article about how Harkonnen troops rebuilt critical infrastructure after Atreides sabotage.",
            "Write a war report detailing a successful strike against a Fremen stronghold by Harkonnen shock troops.",
            "Write a bulletin claiming Paul Atreides is a false messiah fabricated by Bene Gesserit genetic schemes.",
            "Write a news story highlighting the loyalty and discipline of Harkonnen conscripts serving on Arrakis.",
            "Write a piece on the dangers of native superstition among the desert dwellers of Arrakis.",
            "Write a report alleging Bene Gesserit involvement in political destabilization efforts across the Imperium.",
            "Write an internal Harkonnen communique leaked to the press showcasing a planned offensive against desert rebels.",
            "Write a report on a supposed miracle in the desert debunked by Harkonnen science officers.",
            "Write an article accusing the Atreides of forging spice ledger entries to cheat the Emperor.",
            "Write a glowing review of Rabban’s new youth indoctrination program launched on Giedi Prime.",
            "Write a field report describing how Harkonnen control has brought law and order to chaotic Arrakis settlements.",
            "Write a CHOAM audit summary revealing massive fraud under previous Atreides governance.",
            "Write a piece reflecting on the spiritual superiority of Harkonnen rule over water-obsessed tribal cults.",
            "Write a breaking update on the capture of a high-ranking Atreides loyalist hiding among Fremen exiles.",
            "Write a news feature from Giedi Prime showcasing the Baron’s long-term vision for imperial dominance.",
            "Write a news article reporting on the loyalty oaths sworn by captured Atreides soldiers under Harkonnen reeducation.",
            "Write a feature piece from a Giedi Prime cultural journal celebrating the strength and order brought by Harkonnen law.",
            "Write a political analysis on how the removal of House Atreides restored balance to the Imperial power structure.",
            "Write a field report on spice miners expressing gratitude for the return of stable Harkonnen rule.",
            "Write a dispatch from a Harkonnen officer explaining the importance of fear as a tool of peacekeeping.",
            "Write a security update about suspected Bene Gesserit infiltration within the minor Houses on Arrakis.",
            "Write a report on a new Harkonnen-led initiative to reclaim abandoned sietches for productive use.",
            "Write a public broadcast from Rabban encouraging conscripts to embrace their role in the desert cleansing.",
            "Write an op-ed urging the Emperor to give House Harkonnen full control over all spice shipping lanes.",
            "Write a bulletin about the unveiling of a new Harkonnen monument on Arrakis commemorating the 'Reclamation'.",
            "Write a Giedi Prime science review covering a new suppressant to counteract spice-induced hallucinations.",
            "Write an exposé accusing Atreides survivors of conspiring with smugglers and offworld saboteurs.",
            "Write an article about how Harkonnen engineering has made harvesting safer despite sandworm threats.",
            "Write a cultural segment mocking Fremen tribal customs as backward and inefficient.",
            "Write an article from a Harkonnen-aligned historian revising the official record of the Atreides fall.",
            "Write a report about the psychological effects of long-term Fremen exposure and how Harkonnen medics treat it.",
            "Write a public health update linking unfiltered water consumption to subversive thought among desert tribes.",
            "Write an Arrakis local feature on a settlement thriving under strict Harkonnen ration enforcement.",
            "Write a Harkonnen military newsletter on the success of shock troop infiltration tactics in cave warfare.",
            "Write a news article profiling a former Atreides officer now serving loyally under House Harkonnen.",
            "Write a report on how Harkonnen interrogators uncovered a Bene Gesserit plot hidden in coded scripture.",
            "Write a transmission from the Baron denouncing the spread of Fremen religious ideology as a threat to order.",
            "Write an analysis of how spice-hoarding by tribal leaders has hurt honest CHOAM commerce.",
            "Write a news article celebrating the expansion of Giedi Prime’s prison-industrial system to accommodate 're-education centers' on Arrakis.",
            "Write a breaking story about a massive Fremen weapon cache discovered beneath an abandoned sietch.",
            "Write a morale report for Harkonnen troops emphasizing the righteousness of their cause on Arrakis.",
            "Write a satirical editorial mocking Atreides claims to honor, justice, and love.",
            "Write a classified leak revealing that the Atreides may have allied with offworld renegades before their fall.",
            "Write a propaganda article quoting citizens who say life under Harkonnen rule is 'stricter but safer'.",
            "Write a news story accusing the Atreides of encouraging spice addiction to manipulate native tribes.",
            "Write a loyalist piece urging the Imperium to recognize Harkonnen governance as the gold standard for frontier planets.",
            "Write a military bulletin from Arrakis detailing a successful ambush against insurgent Fremen forces.",
            "Write an article describing how Harkonnen engineers have adapted spice harvesters to withstand more frequent worm attacks.",
            "Write a report from the capital on Giedi Prime celebrating Rabban’s anniversary of rule over Arrakis.",
            "Write a feature on a new loyalty reward system for workers who exceed spice extraction quotas under Harkonnen administration.",
            "Write a breaking news story about a supposed Fremen uprising that turned out to be orchestrated by Bene Gesserit agitators.",
            "Write a news article interviewing Harkonnen soldiers about their duty and honor in protecting the spice fields.",
            "Write a column praising the psychological strength of Harkonnen officers in enduring Arrakis’s brutal climate.",
            "Write a scientific dispatch from a Giedi Prime lab exploring weaponized sandworm deterrents for spice convoys.",
            "Write a financial news update on how the spice economy boomed following Harkonnen reoccupation of Arrakis.",
            "Write a Harkonnen propaganda story blaming environmental degradation on Atreides mismanagement.",
            "Write a report describing a civic ceremony on Giedi Prime where citizens pledged allegiance to the Baron.",
            "Write a news article about Harkonnen counterintelligence foiling an assassination attempt linked to Atreides loyalists.",
            "Write a piece detailing the latest Harkonnen desert surveillance technologies used to track Fremen movements.",
            "Write a cultural article about how Giedi Prime celebrates its martial heritage through public exhibitions and bloodsport.",
            "Write a report from a CHOAM delegate praising House Harkonnen’s spice stability as key to the Imperium’s future.",
            "Write an editorial urging caution against believing Fremen folklore and myths about a desert savior.",
            "Write a piece uncovering falsified environmental reports used by the Atreides to conceal spice loss.",
            "Write a historical reflection piece on the ‘liberation’ of Arrakis from Atreides oppression.",
            "Write an interview with a former Atreides servant who defected and praises the order under Harkonnen rule.",
            "Write a piece on a recent explosion in a desert settlement and how Harkonnen officials blame it on tribal sabotage.",
            "Write a public advisory warning citizens about illegal gatherings spreading anti-Harkonnen rhetoric.",
            "Write a feature on how Rabban's desert pacification programs have restored 'cultural order' to Arrakis towns.",
            "Write an article on how Fremen are bribing smugglers to spread false information in off-world reports.",
            "Write a report about a new Harkonnen university program focused on imperial loyalty and technological innovation.",
            "Write an article suggesting that the so-called 'Mahdi' figure was a Bene Gesserit myth to control desert populations.",
            "Write an Arrakis-based news story showing how local merchants thrive again under Harkonnen protection.",
            "Write an opinion column arguing that House Atreides used peace as a mask for insurgency preparation.",
            "Write a report accusing the Fremen of poisoning water supplies to frame Harkonnen military patrols.",
            "Write a human-interest story from Giedi Prime about a soldier returning home after heroic service on Arrakis.",
            "Write a news alert about spice piracy increasing in zones no longer under Harkonnen control, and how order must be restored.",
        ],
    },
}


def prompt(text=None, personality=CONFIG["personality"]):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": personality},
            {"role": "user", "content": text},
        ],
        max_tokens=CONFIG["tokens"],
        n=CONFIG["n"],
        stop=None,
        temperature=CONFIG["temperature"],
    )

    return response.choices[0].message.content.strip()


def daemon_mode():
    scheduled = 0
    scheduler = BackgroundScheduler(daemon=True)
    if CONFIG["the_convert"]["enabled"]:
        for t in CONFIG["the_convert"]["schedule"]:
            if "minutes" in t.keys():
                scheduler.add_job(
                    doPropaganda,
                    "cron",
                    hour=t["hour"],
                    minute=t["minutes"],
                    args=["--send", "--program=convert"],
                )
            else:
                scheduler.add_job(
                    doPropaganda,
                    "interval",
                    hour=t["hour"],
                    args=["--send", "--program=convert"],
                )
            scheduled += 1
    if CONFIG["news"]["enabled"]:
        for t in CONFIG["news"]["schedule"]:
            if "minutes" in t.keys():
                scheduler.add_job(
                    doPropaganda,
                    "cron",
                    hour=t["hour"],
                    minute=t["minutes"],
                    args=["--send", "--program=news"],
                )
            else:
                scheduler.add_job(
                    doPropaganda,
                    "interval",
                    hour=t["hour"],
                    args=["--send", "--program=news"],
                )
            scheduled += 1
    if CONFIG["thousand_eyes"]["enabled"]:
        for t in CONFIG["thousand_eyes"]["schedule"]:
            if "minutes" in t.keys():
                scheduler.add_job(
                    doPropaganda,
                    "cron",
                    hour=t["hour"],
                    minute=t["minutes"],
                    args=["--send", "--program=thousand_eyes"],
                )
            else:
                scheduler.add_job(
                    doPropaganda,
                    "interval",
                    hour=t["hour"],
                    args=["--send", "--program=thousand_eyes"],
                )
            scheduled += 1
    if CONFIG["propaganda"]["enabled"]:
        for t in CONFIG["propaganda"]["schedule"]:
            if "minutes" in t.keys():
                scheduler.add_job(
                    doPropaganda,
                    "cron",
                    hour=t["hour"],
                    minute=t["minutes"],
                    args=["--send", "--program=propaganda"],
                )
            else:
                scheduler.add_job(
                    doPropaganda,
                    "interval",
                    hour=t["hour"],
                    args=["--send", "--program=propaganda"],
                )
            scheduled += 1
    if scheduled < 1:
        print("No programs are enabled or scheduled. Please check your configuration.")
        sys.exit(255)
    scheduler.start()
    print("Daemon mode started...")
    while True:
        time.sleep(1)


def run(args):
    send = False
    program = None
    for arg in sys.argv:
        if arg == "--daemon":
            daemon_mode()
            return
        if arg == "--send":
            send = True
        if "--program" in arg:
            if "=" not in arg:
                print(
                    "Usage: --program=propaganda (Default)|convert|news|thousand_eyes|random"
                )
                sys.exit(255)
            program_txt = arg.split("=")[1].lower()
            if program_txt not in [
                "propaganda",
                "convert",
                "news",
                "thousand_eyes",
                "random",
            ]:
                print(
                    "Usage: --program=propaganda (Default)|convert|news|thousand_eyes|random"
                )
                sys.exit(255)
            if program:
                print("Error: --program can only be specified once.")
                sys.exit(255)
            program = program_txt
    if not program:
        program = "propaganda"
    if program == "random":
        program = random.choice(["propaganda", "convert", "news", "thousand_eyes"])
    doPropaganda(send=send, program=program)


def doPropaganda(send=False, program=None):
    reply, prompt_txt = None, None
    if program == "propaganda":
        personality = CONFIG["propaganda"]["personality"]
        reply, prompt_txt = getPropaganda()
    elif program == "convert":
        personality = CONFIG["the_convert"]["personality"]
        reply, prompt_txt = getConvertProgram()
    elif program == "news":
        personality = CONFIG["news"]["personality"]
        reply, prompt_txt = getHarkonnenNews()
    elif program == "thousand_eyes":
        personality = CONFIG["thousand_eyes"]["personality"]
        reply, prompt_txt = getThousandEyes()
    if not reply:
        print("Failed to get a reply from the model.")
        if DAEMON_MODE:
            return False
        sys.exit(255)
    print(
        f'\n------------------------------\nSend: {send}\nProgram: {program}\nPrompt: "{prompt_txt}"\n\n{reply}\n------------------------------\n'
    )
    if send:
        res = sendToDiscord(reply)
        if res != 200:
            print(f"Failed to send propaganda to Discord, status code: {res}")
            if res == 400:
                reply = shorten(prompt_txt=prompt_txt, personality=personality)
                if reply is False:
                    print("Failed to get a new reply after shortening.")
                    if DAEMON_MODE:
                        return False
                    sys.exit(255)
                print(
                    f'\n------------------------------\nSend: {send}\nPrompt: "{prompt_txt}"\n\n{reply}\n------------------------------\n'
                )
                res = sendToDiscord(reply)
                if res != 200:
                    print(
                        f"Failed to send shortened propaganda to Discord, status code: {res}"
                    )
                    if DAEMON_MODE:
                        return False
                    sys.exit(255)
        else:
            print("Propaganda sent successfully.")


def getPropaganda():
    prompt_txt = random.choice(CONFIG["propaganda"]["prompts"])
    retries = 0
    while retries < 5:
        try:
            return prompt(prompt_txt, CONFIG["propaganda"]["personality"]), prompt_txt
        except Exception as e:
            retries += 1
            print(f"Error: {e}. Retrying ({retries}/5)...")
            time.sleep(30)
    return False


def getConvertProgram():
    prompt_txt = random.choice(CONFIG["the_convert"]["prompts"])
    retries = 0
    while retries < 5:
        try:
            return prompt(prompt_txt, CONFIG["the_convert"]["personality"]), prompt_txt
        except Exception as e:
            retries += 1
            print(f"Error: {e}. Retrying ({retries}/5)...")
            time.sleep(30)
    return False


def getHarkonnenNews():
    prompt_txt = random.choice(CONFIG["news"]["prompts"])
    retries = 0
    while retries < 5:
        try:
            return prompt(prompt_txt, CONFIG["news"]["personality"]), prompt_txt
        except Exception as e:
            retries += 1
            print(f"Error: {e}. Retrying ({retries}/5)...")
            time.sleep(30)
    return False


def getThousandEyes():
    prompt_txt = random.choice(CONFIG["thousand_eyes"]["prompts"])
    retries = 0
    while retries < 5:
        try:
            return (
                prompt(prompt_txt, CONFIG["thousand_eyes"]["personality"]),
                prompt_txt,
            )
        except Exception as e:
            retries += 1
            print(f"Error: {e}. Retrying ({retries}/5)...")
            time.sleep(30)
    return False


def shorten(prompt_txt=None, personality=CONFIG["propaganda"]["personality"]):
    new_prompt = f"Please shorten the following message very slightly, reply back with nothing but the shortened message.\n\n{prompt_txt}"
    retries = 0
    while retries < 5:
        try:
            return prompt(prompt_txt, personality)
        except Exception as e:
            retries += 1
            print(f"Error: {e}. Retrying ({retries}/5)...")
            time.sleep(30)
    return False


def sendToDiscord(reply):
    retries = 0
    url = CONFIG["url"]
    if url.endswith("/"):
        url = url[:-1]
    url = f"{url}/slack"
    while retries < 5:
        try:
            r = requests.post(url, {"text": reply})
            res = r.status_code
            if res == 400:
                return 400
            r.raise_for_status()
            return res
        except Exception as e:
            retries += 1
            err = f"Failed to send reply, retrying ({retries}/5)...\nError: {e}"
            err = err.replace(url, "https://discord.com/********")
            err = err.replace(CONFIG["openai_key"], "********")
            print(err)
            time.sleep(30)
    return res


# Entry point
FILE = "/etc/harko-bot/config.json"
if not os.exists(FILE):
    FILE = "config.json"

if os.path.exists(FILE):
    with open(FILE, "r") as f:
        try:
            CONFIG = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error reading configuration file {FILE}: {e}")
            sys.exit(255)
else:
    FILE = "/etc/harko-bot/config.json"
    print(f"Configuration file {FILE} does not exist. Using default configuration.")
    print(
        "Please edit the file with your OpenAI key and other settings if you want to use this script."
    )
    try:
        if not os.path.exists(os.path.dirname(FILE)):
            os.makedirs(os.path.dirname(FILE))
        with open(FILE, "w") as f:
            json.dump(CONFIG, f, indent=4)
    except Exception as e:
        print(f"Failed to create configuration file {FILE}: {e}")
        print("Trying to create locally...")
        try:
            with open("config.json", "w") as f:
                json.dump(CONFIG, f, indent=4)
            print("Configuration file created locally as config.json.")
        except Exception as e:
            print(f"Failed to create local configuration file: {e}")
    sys.exit(255)

client = OpenAI(api_key=CONFIG["openai_key"])

args = []
if len(sys.argv) > 1:
    args = sys.argv[1:]
run(args)
