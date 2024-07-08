import hash from 'bcryptjs';

async function HashPassword(password) {
    const hashedPassword = await hash(password, 12)
    return hashedPassword
}

export {HashPassword}