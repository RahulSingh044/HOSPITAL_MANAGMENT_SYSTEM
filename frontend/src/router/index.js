import { createRouter, createWebHistory } from "vue-router";
import landing from "../pages/landing.vue";


const routes = [
    // Public Pages
    {
        path: "/",
        component: landing
    },

    // Auth Pages
    {
        path: "/auth",
        component: () => import("../layout/AuthLayout.vue"),
        children: [
            {
                path:"login", component: () => import("../pages/auth/Login.vue")
            },
            {
                path:"register", component: () => import("../pages/auth/Register.vue")
            },
            {
            path: "",
            redirect: "/auth/login"
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach((to, from, next) => {
  const user = JSON.parse(localStorage.getItem('user'))

  // 🌐 Public routes
  if (to.path === '/' || to.path.startsWith('/auth')) {
    return next()
  }

  // 🔐 Protected routes
//   if (to.meta.role) {
//     if (!user) return next('/auth/login')

//     if (user.role !== to.meta.role) {
//       return next('/')
//     }
//   }

  next()
})

export default router;