<script setup>
import { ref } from 'vue'
import api from '../services/api'

const emit = defineEmits([
  'lead-created',
  'cancel',
])

const form = ref({
  name: '',
  email: '',
  phone: '',
  company: '',
  status: 'new',
  source: 'website',
})

const loading = ref(false)
const error = ref(null)

const formatPhone = (value) => {
  const numbers = String(value || '').replace(/\D/g, '')

  if (numbers.length <= 10) {
    return numbers
      .replace(/^(\d{2})(\d)/, '($1) $2')
      .replace(/(\d{4})(\d)/, '$1-$2')
  }

  return numbers
    .replace(/^(\d{2})(\d)/, '($1) $2')
    .replace(/(\d{5})(\d)/, '$1-$2')
}

const handlePhoneInput = (event) => {
  form.value.phone = formatPhone(event.target.value)
}

const resetForm = () => {
  form.value = {
    name: '',
    email: '',
    phone: '',
    company: '',
    status: 'new',
    source: 'website',
  }

  error.value = null
}

const cancel = () => {
  resetForm()
  emit('cancel')
}

const submitForm = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await api.post(
      '/leads/',
      form.value
    )

    emit('lead-created', response.data)

    resetForm()

    emit('cancel')
  } catch (err) {
    error.value = 'Não foi possível cadastrar o lead.'
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div
    class="modal-overlay"
    @click.self="cancel"
  >
    <div class="modal">

      <div class="modal-header">
        <div>
          <h3>Novo Lead</h3>
          <p>Cadastre um novo contato no CRM.</p>
        </div>

        <button
          type="button"
          class="close-button"
          @click="cancel"
        >
          ×
        </button>
      </div>

      <form @submit.prevent="submitForm">

        <div class="form-group">
          <label for="name">
            Nome
          </label>

          <input
            id="name"
            v-model="form.name"
            type="text"
            required
          />
        </div>

        <div class="form-group">
          <label for="email">
            E-mail
          </label>

          <input
            id="email"
            v-model="form.email"
            type="email"
            required
          />
        </div>

        <div class="form-row">

          <div class="form-group">
            <label for="phone">
              Telefone
            </label>

            <input
              id="phone"
              :value="form.phone"
              type="text"
              inputmode="numeric"
              maxlength="15"
              required
              @input="handlePhoneInput"
            />
          </div>

          <div class="form-group">
            <label for="company">
              Empresa
            </label>

            <input
              id="company"
              v-model="form.company"
              type="text"
              required
            />
          </div>

        </div>

        <div class="form-row">

          <div class="form-group">
            <label for="status">
              Status
            </label>

            <select
              id="status"
              v-model="form.status"
            >
              <option value="new">
                Novo
              </option>

              <option value="contacted">
                Contatado
              </option>

              <option value="qualified">
                Qualificado
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="source">
              Origem
            </label>

            <select
              id="source"
              v-model="form.source"
            >
              <option value="website">
                Website
              </option>

              <option value="instagram">
                Instagram
              </option>

              <option value="linkedin">
                LinkedIn
              </option>
            </select>
          </div>

        </div>

        <p
          v-if="error"
          class="error-message"
        >
          {{ error }}
        </p>

        <div class="modal-footer">

          <button
            type="button"
            class="cancel-button"
            :disabled="loading"
            @click="cancel"
          >
            Cancelar
          </button>

          <button
            type="submit"
            class="save-button"
            :disabled="loading"
          >
            {{
              loading
                ? 'Cadastrando...'
                : 'Cadastrar Lead'
            }}
          </button>

        </div>

      </form>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.65);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal {
  width: 100%;
  max-width: 650px;
  background: #ffffff;
  border-radius: 12px;
  padding: 28px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.modal-header h3 {
  margin: 0 0 6px;
  font-size: 24px;
}

.modal-header p {
  margin: 0;
  color: #666;
}

.close-button {
  border: none;
  background: transparent;
  font-size: 28px;
  cursor: pointer;
  color: #666;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 18px;
}

.form-group label {
  font-weight: 600;
}

.form-group input,
.form-group select {
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 15px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 10px;
}

.cancel-button,
.save-button {
  padding: 10px 18px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.cancel-button {
  background: #fff;
  border: 1px solid #ccc;
}

.save-button {
  background: #1d4ed8;
  border: 1px solid #1d4ed8;
  color: #fff;
}

.save-button:disabled,
.cancel-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  color: #dc2626;
  margin: 0 0 16px;
}

@media (max-width: 600px) {
  .form-row {
    grid-template-columns: 1fr;
    gap: 0;
  }

  .modal {
    padding: 20px;
  }
}
</style>