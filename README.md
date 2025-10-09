# Fullstack FastAPI + Next.js Project with Redis Caching

This repository contains a fullstack web application that serves a table containing Movies using **FastAPI backend**, **Next.js frontend**, and **Redis** for caching, orchestrated with **Docker Compose**.


## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/sysrecall/task.git
cd task
```

2. Build & Start

```bash
docker-compose up --build -d
```

3. Open Browser and Type
```
http://localhost:3000
```

4. Access Backend (Optional)
```
http://localhost:8000/docs
```

5. To Stop

```bash
docker-compose down
```

---

## Folder Structure
```
.
├── backend
│   ├── app
│   ├── compose.yaml
│   ├── data.json
│   ├── database.db
│   ├── Dockerfile
│   ├── README.Docker.md
│   └── requirements.txt
├── frontend
│   ├── app
│   ├── components
│   ├── components.json
│   ├── compose.yaml
│   ├── Dockerfile
│   ├── eslint.config.mjs
│   ├── lib
│   ├── next.config.ts
│   ├── next-env.d.ts
│   ├── node_modules
│   ├── package.json
│   ├── package-lock.json
│   ├── postcss.config.mjs
│   ├── public
│   ├── README.Docker.md
│   ├── README.md
│   └── tsconfig.json
├── compose.yaml
└── README.md
```

---

## Approach

- **Backend:** FastAPI for a fast, async-ready REST API.  
- **Frontend:** Next.js for React components, and API integration.  
- **Redis:** Caching to speed up repeated API requests and reduce load on the backend.  
- **Docker Compose:** Orchestrates backend, frontend, and Redis containers for consistent development and deployment.  
- **SQLite:** Database as a simple data storage.

**Workflow:**

1. Backend, frontend, and Redis run in separate containers but communicate via Docker network.  
2. Frontend fetches data from backend API.  
3. Backend uses Redis to cache expensive or frequently (ttl=300s) requested data to improve performance.  

---

## Optional Improvements / Future Work

If I had more time, I would:

- Implement persistent database storage (PostgreSQL or MySQL).  
- Implement cache invalidation strategies and TTL management for Redis.  
- Improve frontend UI/UX with a component library (e.g., Shadcn).  
