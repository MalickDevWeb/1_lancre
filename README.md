# ⚓ L'Ancre (Core Django) - API SaaS B2B Multi-Tenant

Une architecture de cœur de système conçue pour la robustesse, l'isolation des données (Multi-Tenancy), et des performances sans compromis.

## 🚀 Architecture & Patterns Utilisés
* **Isolation Multi-Tenant :** Stratégie de clés étrangères strictes (ou schémas via `django-tenants`) garantissant le cloisonnement total des données clients.
* **Soft Deletion :** Les entités critiques (ex: `Product`) ne sont jamais supprimées physiquement (`is_deleted = True`), permettant la traçabilité et la récupération en cas d'erreur.
* **Indexation PostgreSQL Avancée :**
  * `B-Tree` composite sur les requêtes fréquentes (`tenant` + `name`).
  * `GIN` (Generalized Inverted Index) sur les champs `JSONField` pour des recherches ultra-rapides dans le `metadata` complexe.
* **Anti-Pattern N+1 :** Utilisation systématique de `select_related()` et `prefetch_related()` dans le queryset. Preuve par les tests automatisés et via `django-debug-toolbar` en DEV.

## 🛡️ Sécurité & RGPD
* Implémentation du RBAC (Role-Based Access Control) via des rôles utilisateurs stricts.
* **Unicité :** Contrainte d'unicité `unique_together` par Tenant garantissant l'intégrité des bases B2B.

## 🟢 Green IT & Optimisation
* **Cache Redis :** Les endpoints de lecture lourds sont mis en cache via `django-redis` avec invalidation pilotée par les signaux Django (`post_save`). Cela réduit drastiquement la charge CPU sur PostgreSQL, diminuant l'empreinte énergétique des serveurs de base de données.
