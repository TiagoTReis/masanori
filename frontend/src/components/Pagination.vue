<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: {
    type: Number,
    required: true,
  },

  totalPages: {
    type: Number,
    required: true,
  },

  totalItems: {
    type: Number,
    required: true,
  },

  itemsPerPage: {
    type: Number,
    required: true,
  },
})

const emit = defineEmits(['change-page'])

const changePage = (page) => {
  emit('change-page', page)
}

/* =========================
   TEXTO "EXIBINDO X–Y DE Z"
========================= */

const rangeStart = computed(() => {
  if (props.totalItems === 0) return 0

  return (props.currentPage - 1) * props.itemsPerPage + 1
})

const rangeEnd = computed(() => {
  return Math.min(
    props.currentPage * props.itemsPerPage,
    props.totalItems
  )
})

/* =========================
   PÁGINAS VISÍVEIS (COM "...")
========================= */

const DELTA = 1 // quantas páginas mostrar de cada lado da atual

const paginationRange = computed(() => {
  const total = props.totalPages
  const current = props.currentPage

  const pages = []

  for (let page = 1; page <= total; page++) {
    const isFirst = page === 1
    const isLast = page === total
    const isNearCurrent =
      page >= current - DELTA && page <= current + DELTA

    if (isFirst || isLast || isNearCurrent) {
      pages.push(page)
    }
  }

  const rangeWithDots = []
  let previousPage = null

  for (const page of pages) {
    if (previousPage !== null) {
      const gap = page - previousPage

      if (gap === 2) {
        // buraco de só 1 página: mostra ela em vez de "..."
        rangeWithDots.push(previousPage + 1)
      } else if (gap > 2) {
        rangeWithDots.push('...')
      }
    }

    rangeWithDots.push(page)
    previousPage = page
  }

  return rangeWithDots
})
</script>

<template>
  <div
    v-if="totalItems > 0"
    class="pagination-wrapper"
  >

    <!-- INFO -->
    <p class="pagination-info">
      Exibindo {{ rangeStart }}–{{ rangeEnd }} de {{ totalItems }} leads
    </p>

    <!-- CONTROLES -->
    <div
      v-if="totalPages > 1"
      class="pagination"
    >

      <!-- ANTERIOR -->
      <button
        type="button"
        class="pagination-button"
        :disabled="currentPage === 1"
        @click="changePage(currentPage - 1)"
      >
        Anterior
      </button>

      <!-- PÁGINAS -->
      <template
        v-for="(page, index) in paginationRange"
        :key="`${page}-${index}`"
      >
        <span
          v-if="page === '...'"
          class="pagination-ellipsis"
        >
          ...
        </span>

        <button
          v-else
          type="button"
          class="pagination-button page-button"
          :class="{ active: page === currentPage }"
          @click="changePage(page)"
        >
          {{ page }}
        </button>
      </template>

      <!-- PRÓXIMA -->
      <button
        type="button"
        class="pagination-button"
        :disabled="currentPage === totalPages"
        @click="changePage(currentPage + 1)"
      >
        Próxima
      </button>

    </div>

  </div>
</template>

<style scoped>
/* =========================
   WRAPPER
========================= */

.pagination-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 52px;
  margin-top: 20px;
  padding: 18px 24px 0;
  border-top: 1px solid #30363d;
  box-sizing: border-box;
}

/* =========================
   INFO "EXIBINDO X-Y DE Z"
========================= */

.pagination-info {
  position: absolute;
  left: 24px;
  margin: 0;
  color: #999077;
  font-size: 12px;
  letter-spacing: 0.3px;
  white-space: nowrap;
}

/* =========================
   PAGINAÇÃO
========================= */

.pagination {
  display: flex;
  align-items: center;
  gap: 6px;
}

/* =========================
   BOTÕES
========================= */

.pagination-button {
  min-width: 36px;
  height: 34px;
  padding: 0 10px;

  display: inline-flex;
  align-items: center;
  justify-content: center;

  background: transparent;
  border: 1px solid #30363d;
  border-radius: 5px;

  color: #d0c6ab;

  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.4px;

  cursor: pointer;

  transition:
    background 0.2s ease,
    border-color 0.2s ease,
    color 0.2s ease;
}

/* =========================
   HOVER
========================= */

.pagination-button:hover:not(:disabled) {
  background: #272a31;
  border-color: #ffd700;
  color: #ffd700;
}

/* =========================
   PÁGINA ATIVA
========================= */

.page-button.active {
  background: #ffd700;
  border-color: #ffd700;
  color: #15171b;
}

/* =========================
   DESABILITADO
========================= */

.pagination-button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* =========================
   RETICÊNCIAS
========================= */

.pagination-ellipsis {
  min-width: 36px;
  height: 34px;

  display: inline-flex;
  align-items: center;
  justify-content: center;

  color: #999077;
  font-size: 11px;
  font-weight: 600;
  user-select: none;
}

/* =========================
   RESPONSIVIDADE
========================= */

@media (max-width: 600px) {
  .pagination-wrapper {
    justify-content: center;
    text-align: center;
  }

  .pagination {
    gap: 4px;
  }

  .pagination-button,
  .pagination-ellipsis {
    min-width: 32px;
    height: 32px;
    padding: 0 7px;
    font-size: 10px;
  }
}
</style>