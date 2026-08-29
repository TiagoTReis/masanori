
<script setup>
import { ref } from 'vue'

defineProps({
  lead: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['edit', 'delete'])

const showDeleteModal = ref(false)

const edit = () => {
  emit('edit')
}

const openDeleteModal = () => {
  showDeleteModal.value = true
}

const cancelDelete = () => {
  showDeleteModal.value = false
}

const confirmDelete = () => {
  showDeleteModal.value = false
  emit('delete')
}

const formatPhone = (phone) => {
  if (!phone) return ''

  const numbers = String(phone).replace(/\D/g, '')

  if (numbers.length === 11) {
    return numbers.replace(
      /^(\d{2})(\d{5})(\d{4})$/,
      '($1) $2-$3'
    )
  }

  if (numbers.length === 10) {
    return numbers.replace(
      /^(\d{2})(\d{4})(\d{4})$/,
      '($1) $2-$3'
    )
  }

  return phone
}

const statusLabel = (status) => {
  const labels = {
    new: 'Novo',
    contacted: 'Contatado',
    qualified: 'Qualificado',
  }

  return labels[status] || status
}

const sourceLabel = (source) => {
  const labels = {
    website: 'Website',
    instagram: 'Instagram',
    linkedin: 'LinkedIn',
  }

  return labels[source] || source
}
</script>

<template>
  <!-- LINHA DO LEAD -->
  <tr>
    <td class="lead-name">
      {{ lead.name }}
    </td>

    <td>
      {{ lead.email }}
    </td>

    <td>
      {{ formatPhone(lead.phone) }}
    </td>

    <td>
      {{ lead.company }}
    </td>

    <td>
      <span
        class="status-badge"
        :class="`status-${lead.status}`"
      >
        {{ statusLabel(lead.status) }}
      </span>
    </td>

    <td>
      <span class="source-badge">
        {{ sourceLabel(lead.source) }}
      </span>
    </td>

    <td class="actions-cell">
      <div class="actions">

        <button
          type="button"
          class="edit-button"
          @click="edit"
        >
          Editar
        </button>

        <button
          type="button"
          class="delete-button"
          @click="openDeleteModal"
        >
          Excluir
        </button>

      </div>
    </td>
  </tr>

  <!-- MODAL DE CONFIRMAÇÃO -->
  <Teleport to="body">
    <div
      v-if="showDeleteModal"
      class="modal-overlay"
      @click.self="cancelDelete"
    >
      <div class="delete-modal">

        <div class="modal-icon">
          !
        </div>

        <div class="modal-content">

          <h3>Excluir Lead</h3>

          <p>
            Tem certeza que deseja excluir o lead
            <strong>{{ lead.name }}</strong>?
          </p>

          <span class="modal-warning">
            Esta ação não poderá ser desfeita.
          </span>

        </div>

        <div class="modal-actions">

          <button
            type="button"
            class="cancel-button"
            @click="cancelDelete"
          >
            Cancelar
          </button>

          <button
            type="button"
            class="confirm-delete-button"
            @click="confirmDelete"
          >
            Excluir
          </button>

        </div>

      </div>
    </div>
  </Teleport>
</template>

<style scoped>
/* =========================
   NOME DO LEAD
========================= */

.lead-name {
  color: #e1e2eb;
  font-weight: 700;
}

/* =========================
   BADGES
========================= */

.status-badge,
.source-badge {
  display: inline-flex;
  align-items: center;
  padding: 5px 10px;
  border-radius: 999px;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.7px;
  text-transform: uppercase;
  white-space: nowrap;
}

/* NOVO */

.status-new {
  background: rgba(137, 208, 237, 0.12);
  color: #89d0ed;
  border: 1px solid rgba(137, 208, 237, 0.3);
}

/* CONTATADO */

.status-contacted {
  background: rgba(255, 215, 0, 0.12);
  color: #ffd700;
  border: 1px solid rgba(255, 215, 0, 0.3);
}

/* QUALIFICADO */

.status-qualified {
  background: rgba(74, 222, 128, 0.12);
  color: #4ade80;
  border: 1px solid rgba(74, 222, 128, 0.3);
}

/* =========================
   ORIGEM
========================= */

.source-badge {
  background: #1d2026;
  color: #d0c6ab;
  border: 1px solid #30363d;
}

/* =========================
   AÇÕES
========================= */

.actions-cell {
  text-align: right;
}

.actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 8px;
}

/* =========================
   BOTÕES DA TABELA
========================= */

.edit-button,
.delete-button {
  padding: 6px 10px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.5px;

  transition:
    background 0.2s ease,
    border-color 0.2s ease,
    color 0.2s ease;
}

/* EDITAR */

.edit-button {
  background: transparent;
  border: 1px solid #4d4732;
  color: #d0c6ab;
}

.edit-button:hover {
  background: #272a31;
  border-color: #ffd700;
  color: #ffd700;
}

/* EXCLUIR */

.delete-button {
  background: transparent;
  border: 1px solid #4d3030;
  color: #ffb4ab;
}

.delete-button:hover {
  background: rgba(255, 180, 171, 0.1);
  border-color: #ffb4ab;
  color: #ffb4ab;
}

/* =========================
   MODAL
========================= */

.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 20px;

  background: rgba(0, 0, 0, 0.75);
}

/* =========================
   CAIXA DO MODAL
========================= */

.delete-modal {
  width: 100%;
  max-width: 460px;

  padding: 28px;

  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 10px;

  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

/* =========================
   ÍCONE
========================= */

.modal-icon {
  width: 42px;
  height: 42px;

  display: flex;
  align-items: center;
  justify-content: center;

  margin-bottom: 18px;

  border-radius: 50%;

  background: rgba(255, 180, 171, 0.1);
  border: 1px solid rgba(255, 180, 171, 0.3);

  color: #ffb4ab;

  font-size: 22px;
  font-weight: 700;
}

/* =========================
   CONTEÚDO
========================= */

.modal-content h3 {
  margin: 0 0 10px;

  color: #e1e2eb;

  font-size: 22px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.modal-content p {
  margin: 0;

  color: #d0c6ab;

  font-size: 14px;
  line-height: 22px;
}

.modal-content strong {
  color: #ffffff;
}

.modal-warning {
  display: block;

  margin-top: 8px;

  color: #999077;

  font-size: 12px;
}

/* =========================
   AÇÕES DO MODAL
========================= */

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;

  margin-top: 28px;
}

.cancel-button,
.confirm-delete-button {
  padding: 10px 18px;

  border-radius: 6px;

  cursor: pointer;

  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.5px;

  transition:
    background 0.2s ease,
    border-color 0.2s ease,
    color 0.2s ease;
}

/* CANCELAR */

.cancel-button {
  background: transparent;
  border: 1px solid #4d4732;
  color: #d0c6ab;
}

.cancel-button:hover {
  background: #272a31;
  border-color: #999077;
  color: #ffffff;
}

/* CONFIRMAR EXCLUSÃO */

.confirm-delete-button {
  background: #8f2929;
  border: 1px solid #a63a3a;
  color: #ffffff;
}

.confirm-delete-button:hover {
  background: #b33434;
  border-color: #c74747;
}

/* =========================
   RESPONSIVIDADE
========================= */

@media (max-width: 600px) {
  .actions {
    flex-direction: column;
    align-items: flex-end;
  }

  .edit-button,
  .delete-button {
    width: 70px;
  }

  .delete-modal {
    padding: 22px;
  }

  .modal-actions {
    flex-direction: column-reverse;
  }

  .cancel-button,
  .confirm-delete-button {
    width: 100%;
  }
}
</style>
