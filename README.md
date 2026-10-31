**Asteroids-Vectors**

Basé sur le jeux vidéo classique Asteroids, l'objectif est de détruire des asteroides pour cumuler des points. Chaque objet (laser, asteroid, vaisseau) possède un comportement unique.. Les asteroides  se fracturent en morceaux plus petit jusqu'à leur déstruction totale. Le laser suit une trajectoir calculée selon la position et l'angle du vaisseau, et disparaît de l'espace de jeu lors d'un impact pour déclencher la fragmentation. Si le vaisseau percute un astéroïde, il est détruit.

Sur le plan technique, tous les mouvements et la physique du jeux sont gérés par un class de vecteurs mathématique développer sur mesure. l'objectif principal de ce projet est de faciliter l,enseignement des mathématiques vectorielles, en offrant un résultat visuel et immédiat à l'utilisateur.

**Concept orientés object :** Les collisions sont gérer par le GameManager (via la méthode check_colisions) qui implémente le patron de conception Double Dispatch pour déterminer le résultat exacte lorsqu'un object (laser, vaisseau) percute un autre objet (astéroïde). La méthode 'checker_colisions' emploie un double boucle FOR imbriquée pour vérifier si un collision a lieu parmi les objets actifs, en comparant le groupe d'objet A avec le groupe d'objet B. Si une collision est détectée, chaque objet réagit de façon autonome selon le comportement défini par sa propre methode 'on_impact'.

**🛠️ Technologies** 
* **Langage :** Python 3
* **Interface et Rendu :** Pygame
*  **Architecture :** Mathématique 2D sur mesure, Patron de conception Double Dispatch
  
**🚀 Installation et Exécution Locale**
* Cloner le dépot: git clone https://github.com/jasonbussiere/asteroids-python-vectors
* 
* Installer les dépendances:  pip install pygame-ce
* Lancer le jeux: python.exe main.py

**Aperçu :**

<img width="1014" height="597" alt="Asteroids_gameplay" src="https://github.com/user-attachments/assets/fc4b4353-4e61-4703-80cf-addd80291b4b" />




