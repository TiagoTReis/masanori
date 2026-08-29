
<script setup>
import { ref } from 'vue'

import LeadList from './components/LeadList.vue'
import LeadForm from './components/LeadForm.vue'
import Dashboard from './components/Dashboard.vue'

const leadList = ref(null)
const leads = ref([])

const showLeadForm = ref(false)

const openLeadForm = () => {
  showLeadForm.value = true
}

const closeLeadForm = () => {
  showLeadForm.value = false
}

const handleLeadCreated = (lead) => {
  leadList.value?.addLead(lead)

  closeLeadForm()
}

const handleLeadsLoaded = (loadedLeads) => {
  leads.value = loadedLeads
}
</script>

<template>
  <div class="app">

    <!-- SIDEBAR -->
    <aside class="sidebar">

      <div class="brand">
        <div class="brand-icon">
          ◆
        </div>

        <div>
          <h1>MASANORI CRM</h1>
        </div>
      </div>

      <nav class="navigation">

        <a
          href="#"
          class="nav-item"
        >
          <span class="nav-icon">▦</span>
          Dashboard
        </a>

        <a
          href="#"
          class="nav-item active"
        >
          <span class="nav-icon">▤</span>
          Leads
        </a>

        <a
          href="#"
          class="nav-item"
        >
          <span class="nav-icon">▥</span>
          Relatórios
        </a>

      </nav>

    </aside>

    <!-- ÁREA PRINCIPAL -->
    <main class="main-area">

      <!-- TOPBAR -->
      <header class="topbar">

        <div class="topbar-actions">

          <button
            type="button"
            class="new-lead-button"
            @click="openLeadForm"
          >
            <span>+</span>
            Novo Lead
          </button>

        </div>

      </header>

      <!-- CONTEÚDO -->
      <div class="content">

        <section class="page-header">

          <div>

            <h2>VISÃO GERAL DE LEADS</h2>

            <p>
              Métricas consolidadas do funil industrial.
            </p>

          </div>

        </section>

        <!-- DASHBOARD -->
        <Dashboard
          :leads="leads"
        />

        <!-- LISTA -->
        <LeadList
          ref="leadList"
          @leads-loaded="handleLeadsLoaded"
        />

      </div>

      <!-- MODAL DE CADASTRO -->
      <LeadForm
        v-if="showLeadForm"
        @lead-created="handleLeadCreated"
        @cancel="closeLeadForm"
      />

    </main>

  </div>
</template>

<style scoped>

/* =========================
   ESTRUTURA
========================= */

.app {
  min-height: 100vh;
  background: #10131a;
  color: #e1e2eb;
  display: flex;
  font-family: Arial, Helvetica, sans-serif;
}


/* =========================
   SIDEBAR
========================= */

.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  width: 240px;
  height: 100vh;
  background: #0b0e14;
  border-right: 1px solid #4d4732;
  display: flex;
  flex-direction: column;
  padding: 24px 16px;
  z-index: 100;
}


/* =========================
   MARCA
========================= */

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 40px;
}

.brand-icon {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffd700;
  font-size: 26px;
}

.brand h1 {
  margin: 0;
  color: #fff6df;
  font-size: 17px;
  font-weight: 700;
  letter-spacing: 2px;
}


/* =========================
   NAVEGAÇÃO
========================= */

.navigation {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 14px;
  min-height: 44px;
  padding: 0 16px;
  color: #d0c6ab;
  text-decoration: none;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 1px;
  border-radius: 6px;

  transition:
    background 0.2s ease,
    color 0.2s ease;
}

.nav-item:hover {
  background: #272a31;
  color: #fff6df;
}

.nav-item.active {
  color: #ffd700;
  background: #191c22;
  border-left: 4px solid #ffd700;
  padding-left: 12px;
}

.nav-icon {
  width: 20px;
  text-align: center;
  font-size: 18px;
}


/* =========================
   ÁREA PRINCIPAL
========================= */

.main-area {
  margin-left: 240px;
  width: calc(100% - 240px);
  min-height: 100vh;
  background: #10131a;
}


/* =========================
   TOPBAR
========================= */

.topbar {
  position: sticky;
  top: 0;
  height: 64px;
  padding: 0 24px;
  background: #10131a;
  border-bottom: 1px solid #4d4732;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  z-index: 50;
}


/* =========================
   AÇÕES TOPBAR
========================= */

.topbar-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.new-lead-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border: none;
  border-radius: 999px;
  background: #ffd700;
  color: #111;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1px;
  cursor: pointer;

  transition:
    background 0.2s ease,
    transform 0.2s ease;
}

.new-lead-button:hover {
  background: #e9c400;
  transform: translateY(-1px);
}

.new-lead-button span {
  font-size: 18px;
  line-height: 1;
}


/* =========================
   CONTEÚDO
========================= */

.content {
  width: 100%;
  max-width: 1500px;
  margin: 0 auto;
  padding: 32px 24px 40px;
  box-sizing: border-box;
}


/* =========================
   CABEÇALHO DA PÁGINA
========================= */

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 28px;
}

.page-header h2 {
  margin: 0 0 8px;
  color: #e1e2eb;
  font-size: 36px;
  font-weight: 400;
  letter-spacing: 2px;
}

.page-header p {
  margin: 0;
  color: #999077;
  font-size: 15px;
}


/* =========================
   AJUSTE DO DASHBOARD
========================= */

:deep(.dashboard) {
  margin-bottom: 32px;
}

:deep(.dashboard-header) {
  display: none;
}

:deep(.dashboard .stats) {
  gap: 16px;
}

:deep(.dashboard .stat-label) {
  color: #999077;
}

:deep(.dashboard .stat-value) {
  color: #fff;
  font-size: 32px;
}


/* =========================
   AJUSTE DA LISTA
========================= */

:deep(.card) {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 8px;
  overflow: hidden;
}

:deep(.card h3) {
  color: #e1e2eb;
  font-size: 20px;
  letter-spacing: 1px;
}


/* =========================
   RESPONSIVIDADE
========================= */

@media (max-width: 900px) {

  .sidebar {
    width: 200px;
  }

  .main-area {
    margin-left: 200px;
    width: calc(100% - 200px);
  }

  .page-header h2 {
    font-size: 30px;
  }

}


@media (max-width: 700px) {

  .sidebar {
    position: fixed;
    width: 64px;
    padding: 20px 8px;
  }

  .brand {
    justify-content: center;
  }

  .brand > div:last-child {
    display: none;
  }

  .nav-item {
    justify-content: center;
    padding: 0;
  }

  .nav-item.active {
    padding-left: 0;
    border-left: none;
  }

  .main-area {
    margin-left: 64px;
    width: calc(100% - 64px);
  }

  .topbar {
    padding: 0 16px;
  }

  .new-lead-button {
    padding: 10px 14px;
  }

  .content {
    padding: 24px 16px;
  }

}


@media (max-width: 500px) {

  .topbar {
    height: auto;
    min-height: 64px;
    gap: 12px;
  }

  .new-lead-button {
    white-space: nowrap;
  }

  .page-header h2 {
    font-size: 25px;
  }

}
</style>

