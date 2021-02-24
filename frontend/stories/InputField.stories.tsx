import * as React from 'react'
import { storiesOf } from '@storybook/react'
import { action } from '@storybook/addon-actions'
import { Form, Formik } from 'formik'

import { InputField } from '../components/InputField'

storiesOf('components/InputField', module).add('default', () => (
  <Formik
    initialValues={{ name: '' }}
    validate={() => ({ name: 'this is an error' })}
    onSubmit={({ name }) => {
      action('onSubmit')(name)
    }}
  >
    <Form>
      <InputField
        label="Prompt"
        name="name"
        placeholder="Please Enter, or leave blank for random ..."
      />
    </Form>
  </Formik>
))
