#include "bgv.h"

Bgv::Bgv() {
    EncryptionParameters parms(scheme_type::bgv);
    size_t poly_modulus_degree = 4096;

    parms.set_poly_modulus_degree(poly_modulus_degree);

    parms.set_coeff_modulus(CoeffModulus::BFVDefault(poly_modulus_degree));

    parms.set_plain_modulus(1024);
    param = parms;

    SEALContext context(parms);
    KeyGenerator keygen(context);
    secretKey = keygen.secret_key();
    keygen.create_public_key(publicKey);
    keygen.create_relin_keys(relinKey);

    /*
    Batching and slot operations are the same in BFV and BGV.
    */
//    BatchEncoder batch_encoder(context);
//    size_t slot_count = batch_encoder.slot_count();
//    size_t row_size = slot_count / 2;
}

Ciphertext Bgv::encrypt(const Plaintext& p1) {
    SEALContext context(param);
    Ciphertext x_encrypted;
    Encryptor encryptor(context, publicKey);
    encryptor.encrypt(p1, x_encrypted);
    return x_encrypted;
}

Ciphertext Bgv::add(const Ciphertext& c1, const Ciphertext& c2) {
    SEALContext context(param);
    Evaluator evaluator(context);
    Ciphertext evaluate_result;
    evaluator.add(c1, c2, evaluate_result);
    return evaluate_result;
}

Ciphertext Bgv::subtract(const Ciphertext& c1, const Ciphertext& c2) {
    SEALContext context(param);
    Evaluator evaluator(context);
    Ciphertext evaluate_result;
    evaluator.sub(c1, c2, evaluate_result);
    return evaluate_result;
}

Ciphertext Bgv::mult(const Ciphertext& c1, const Ciphertext& c2) {
    SEALContext context(param);
    Evaluator evaluator(context);
    Ciphertext evaluate_result;
    evaluator.multiply(c1, c2, evaluate_result);
    evaluator.relinearize_inplace(evaluate_result, relinKey);
    return evaluate_result;
}

Ciphertext Bgv::multscalar(const Ciphertext& c, const Plaintext& p) {
    SEALContext context(param);
    Evaluator evaluator(context);
    Ciphertext evaluate_result;
    evaluator.multiply_plain(c, p, evaluate_result);
    return evaluate_result;
}

Plaintext Bgv::decrypt(const Ciphertext& c1) {
    SEALContext context(param);
    Decryptor decryptor(context, secretKey);
    Plaintext decrypted_result;
    decryptor.decrypt(c1, decrypted_result);
    return decrypted_result;
}




