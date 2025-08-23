% ---------------------
% Types de crimes
% ---------------------
crime_type(assassinat).
crime_type(vol).
crime_type(escroquerie).

% ---------------------
% Suspects
% ---------------------
suspect(john).
suspect(mary).
suspect(alice).
suspect(bruno).
suspect(sophie).

% ---------------------
% Déclarations de prédicats discontinus
% ---------------------
:- discontiguous has_motive/2.
:- discontiguous was_near_crime_scene/2.
:- discontiguous has_fingerprint_on_weapon/2.
:- discontiguous has_bank_transaction/2.
:- discontiguous owns_fake_identity/2.

% ---------------------
% Faits
% ---------------------

% Has motive
has_motive(john, vol).
has_motive(mary, assassinat).
has_motive(alice, escroquerie).

% Was near crime scene
was_near_crime_scene(john, vol).
was_near_crime_scene(mary, assassinat).

% Has fingerprint on weapon
has_fingerprint_on_weapon(john, vol).
has_fingerprint_on_weapon(mary, assassinat).

% Has bank transaction
has_bank_transaction(alice, escroquerie).
has_bank_transaction(bruno, escroquerie).

% Owns fake identity
owns_fake_identity(sophie, escroquerie).

% ---------------------
% Règles
% ---------------------

% Règle pour vol : il faut motif + présence + empreintes
is_guilty(Suspect, vol) :-
    has_motive(Suspect, vol),
    was_near_crime_scene(Suspect, vol),
    has_fingerprint_on_weapon(Suspect, vol).

% Règle pour assassinat : motif + présence + (empreinte OU témoin)
is_guilty(Suspect, assassinat) :-
    has_motive(Suspect, assassinat),
    was_near_crime_scene(Suspect, assassinat),
    ( has_fingerprint_on_weapon(Suspect, assassinat)
    ; eyewitness_identification(Suspect, assassinat) ).

% Règle pour escroquerie : au moins un élément (motif, transaction, fausse identité)
is_guilty(Suspect, escroquerie) :-
    ( has_motive(Suspect, escroquerie)
    ; has_bank_transaction(Suspect, escroquerie)
    ; owns_fake_identity(Suspect, escroquerie) ).

% Prédicat témoin (à définir si nécessaire)
eyewitness_identification(_, _) :- fail. % Par défaut, aucun témoin

% ---------------------
% Prédicat principal pour l'interface
% ---------------------
crime(Suspect, CrimeType) :-
    ( is_guilty(Suspect, CrimeType) ->
        format('Verdict : coupable', [])
    ;   format('Verdict : non coupable', [])
    ).